from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
import sqlite3
from datetime import datetime
from flask_mail import Mail, Message
import json
import os
import io

app = Flask(__name__)
app.secret_key = 'super-secret-key-change-this-!@#123'

# إعداد البريد الإلكتروني (يُعدل لاحقاً)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'
mail = Mail(app)

# مجلد رفع الملفات الطبية
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# -------------------- قاعدة المعارف الطبية للروبوت --------------------
MEDICAL_KNOWLEDGE = {
    'صداع': 'الصداع قد يكون ناتجاً عن إجهاد، قلة نوم، أو مشاكل في النظر. اشرب الماء، استرح في مكان هادئ، وإذا تكرر يجب مراجعة طبيب أعصاب.',
    'حمى': 'ارتفاع الحرارة يشير إلى وجود التهاب. يجب قياس الحرارة، تناول خافض حرارة، والإكثار من السوائل. إذا تجاوزت 39 درجة أو استمرت أكثر من 3 أيام، راجع الطبيب.',
    'معدة': 'ألم المعدة قد يكون بسبب سوء هضم، التهاب، أو قرحة. تجنب الأطعمة الحارة والدسمة، وتناول وجبات خفيفة. إذا كان الألم شديداً أو مستمراً، استشر طبيب باطني.',
    'بطن': 'ألم البطن له أسباب عديدة. يُنصح بمراجعة طبيب لتحديد السبب.',
    'ظهر': 'آلام الظهر غالباً بسبب الجلوس الخاطئ أو حمل أشياء ثقيلة. حافظ على استقامة الظهر، مارس تمارين خفيفة. إذا استمر الألم، راجع طبيب عظام.',
    'حساسية': 'الحساسية قد تظهر كطفح جلدي أو عطاس. حدد المسبب وتجنبه، ويمكن استخدام مضادات الهيستامين بعد استشارة الطبيب.',
    'قلب': 'أي ألم في الصدر أو ضيق تنفس يجب أن يؤخذ بجدية. توجه فوراً إلى أقرب طوارئ.',
    'سكري': 'إذا كنت تشعر بالعطش الشديد وكثرة التبول، قد تكون أعراض سكري. راجع طبيب غدد صماء لإجراء الفحوصات.',
    'تنفس': 'ضيق التنفس قد يكون بسبب ربو أو مشكلة قلبية. استشر طبيب صدرية.',
    'عين': 'احمرار أو ألم العين يستدعي فحصاً لدى طبيب عيون.',
    'أسنان': 'ألم الأسنان غالباً تسوس أو التهاب لثة. راجع طبيب أسنان.',
    'نفسية': 'القلق والاكتئاب أمراض حقيقية. تحدث مع طبيب نفسي، فالصحة النفسية مهمة.',
    'عظام': 'آلام المفاصل قد تكون روماتيزم أو خشونة. راجع طبيب عظام أو روماتيزم.',
    'كبد': 'أعراض الكبد تشمل اليرقان والتعب. راجع طبيب باطني فوراً.',
    'كلية': 'آلام الخاصرة مع تغير لون البول قد تشير لمشكلة كلوية. اشرب ماء كثيراً وراجع طبيب.',
    'سرطان': 'أي كتلة غير طبيعية أو فقدان وزن غير مبرر يجب فحصها. الكشف المبكر مهم.',
}
BANNED_WORDS = ['إهانة', 'سب', 'شتم', 'كلمات_بذيئة']

def load_all_files_content():
    all_text = ""
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename.endswith('.txt'):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        all_text += f.read() + "\n"
                except:
                    pass
    return all_text

def analyze_symptoms(text):
    if not text:
        return 'يرجى كتابة الأعراض التي تشعر بها.'
    for word in BANNED_WORDS:
        if word in text:
            return 'عذراً، لا يمكنني الرد على هذا النوع من الكلام. يرجى كتابة أعراض طبية.'
    
    for keyword, response in MEDICAL_KNOWLEDGE.items():
        if keyword in text:
            return response

    files_content = load_all_files_content()
    if files_content:
        sentences = files_content.split('\n')
        relevant = []
        for sentence in sentences:
            if any(word in sentence for word in text.split()):
                relevant.append(sentence.strip())
        if relevant:
            return "بناءً على المعلومات الطبية المرفوعة:\n" + "\n".join(relevant[:3])
        else:
            for sentence in sentences:
                if len(set(text.split()) & set(sentence.split())) > 0:
                    relevant.append(sentence.strip())
            if relevant:
                return "قد تكون الأعراض مرتبطة بـ:\n" + "\n".join(relevant[:2])

    return 'شكراً لتواصلك. يُرجى استشارة الطبيب المختص للحصول على تشخيص دقيق، حيث أن الأعراض قد تكون متداخلة.'

# -------------------- إنشاء قاعدة البيانات --------------------
def init_db():
    conn = sqlite3.connect('medical_center.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    role TEXT,
                    name TEXT,
                    specialty TEXT,
                    email TEXT,
                    phone TEXT,
                    whatsapp TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_name TEXT,
                    patient_email TEXT,
                    patient_phone TEXT,
                    doctor_id INTEGER,
                    date TEXT,
                    time TEXT,
                    description TEXT,
                    status TEXT DEFAULT 'pending',
                    FOREIGN KEY(doctor_id) REFERENCES users(id)
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS disease_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_name TEXT,
                    patient_email TEXT,
                    patient_phone TEXT,
                    specialty TEXT,
                    description TEXT,
                    doctor_id INTEGER,
                    sent_at TEXT,
                    FOREIGN KEY(doctor_id) REFERENCES users(id)
                )''')
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, role, name, email) VALUES (?,?,?,?,?)",
                  ('admin', 'admin123', 'admin', 'AYA Admin', 'admin@aya.com'))
    c.execute("SELECT * FROM users WHERE username='doctor1'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, role, name, specialty, email) VALUES (?,?,?,?,?,?)",
                  ('doctor1', 'doc123', 'doctor', 'د. أحمد', 'جلدية', 'derm@aya.com'))
        c.execute("INSERT INTO users (username, password, role, name, specialty, email) VALUES (?,?,?,?,?,?)",
                  ('doctor2', 'doc123', 'doctor', 'د. سارة', 'عظمية', 'ortho@aya.com'))
        c.execute("INSERT INTO users (username, password, role, name, specialty, email) VALUES (?,?,?,?,?,?)",
                  ('doctor3', 'doc123', 'doctor', 'د. خالد', 'قلبية', 'cardio@aya.com'))
    conn.commit()
    conn.close()

# -------------------- إعدادات النظام (ملف JSON) --------------------
SETTINGS_FILE = 'settings.json'
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}
def save_settings(data):
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# -------------------- مسارات المريض --------------------
@app.route('/')
def index():
    specialties = ['جلدية', 'عظمية', 'قلبية', 'عيون', 'أسنان', 'باطنية', 'نسائية', 'أورام', 'رجالية', 'أعصاب', 'صدرية', 'روماتيزم', 'غدد', 'دم', 'أنف وأذن', 'نفسية']
    conn = sqlite3.connect('medical_center.db')
    c = conn.cursor()
    c.execute("SELECT id, name, specialty FROM users WHERE role='doctor'")
    doctors = c.fetchall()
    conn.close()
    return render_template('index.html', specialties=specialties, doctors=doctors)

@app.route('/book', methods=['POST'])
def book_appointment():
    data = request.form
    conn = sqlite3.connect('medical_center.db')
    c = conn.cursor()
    c.execute("INSERT INTO appointments (patient_name, patient_email, patient_phone, doctor_id, date, time, description) VALUES (?,?,?,?,?,?,?)",
              (data['name'], data['email'], data['phone'], data['doctor'], data['date'], data['time'], data['description']))
    conn.commit()
    conn.close()
    flash('تم إرسال طلب الموعد بنجاح، سيتم إشعارك عند الموافقة', 'success')
    return redirect(url_for('index'))

@app.route('/report', methods=['POST'])
def disease_report():
    data = request.form
    conn = sqlite3.connect('medical_center.db')
    c = conn.cursor()
    doctor_id = data.get('doctor') or None
    specialty = data['specialty']
    if doctor_id:
        c.execute("SELECT email FROM users WHERE id=?", (doctor_id,))
        doc_email = c.fetchone()
    else:
        c.execute("SELECT email FROM users WHERE specialty=? AND role='doctor'", (specialty,))
        doc_email = c.fetchone()
    c.execute("INSERT INTO disease_reports (patient_name, patient_email, patient_phone, specialty, description, doctor_id, sent_at) VALUES (?,?,?,?,?,?,?)",
              (data['name'], data['email'], data['phone'], specialty, data['description'], doctor_id, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()
    if doc_email:
        try:
            msg = Message(f"تقرير طبي جديد - {specialty}", recipients=[doc_email[0]])
            msg.body = f"تقرير من المريض: {data['name']}\nالهاتف: {data['phone']}\nالبريد: {data['email']}\nالتخصص: {specialty}\nالوصف:\n{data['description']}"
            mail.send(msg)
        except Exception as e:
            print("فشل إرسال البريد:", e)
    flash('تم إرسال التقرير بنجاح', 'success')
    return redirect(url_for('index'))

# -------------------- API الروبوت --------------------
@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    symptoms = data.get('symptoms', '')
    reply = analyze_symptoms(symptoms)
    return jsonify({'reply': reply})

# -------------------- مسارات الإدارة --------------------
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('medical_center.db')
        c = conn.cursor()
        c.execute("SELECT id, role, name FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user and user[1] == 'admin':
            session['user_id'] = user[0]
            session['role'] = user[1]
            session['name'] = user[2]
            return redirect(url_for('admin_dashboard'))
        else:
            flash('بيانات الدخول خاطئة أو غير مصرح', 'danger')
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    conn = sqlite3.connect('medical_center.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM appointments WHERE date=?", (datetime.now().strftime("%Y-%m-%d"),))
    today_apps = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM appointments WHERE status='pending'")
    pending = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM appointments WHERE status='completed'")
    completed = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM appointments")
    total_patients = c.fetchone()[0]
    c.execute("SELECT a.id, a.patient_name, a.patient_email, a.patient_phone, u.name as doctor, a.date, a.status FROM appointments a JOIN users u ON a.doctor_id = u.id ORDER BY a.id DESC LIMIT 10")
    appointments = c.fetchall()
    c.execute("SELECT * FROM disease_reports ORDER BY id DESC LIMIT 10")
    reports = c.fetchall()
    c.execute("SELECT id, name, specialty, email, phone, whatsapp FROM users WHERE role='doctor'")
    doctors = c.fetchall()
    conn.close()
    settings = load_settings()
    uploaded_files = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        uploaded_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.txt')]
    return render_template('admin_dashboard.html',
                           today_apps=today_apps,
                           pending=pending,
                           completed=completed,
                           total_patients=total_patients,
                           appointments=appointments,
                           reports=reports,
                           doctors=doctors,
                           settings=settings,
                           uploaded_files=uploaded_files)

@app.route('/admin/approve/<int:appointment_id>')
def approve_appointment(appointment_id):
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    conn = sqlite3.connect('medical_center.db')
    c = conn.cursor()
    c.execute("UPDATE appointments SET status='approved' WHERE id=?", (appointment_id,))
    c.execute("SELECT patient_name, patient_email FROM appointments WHERE id=?", (appointment_id,))
    patient = c.fetchone()
    conn.commit()
    conn.close()
    if patient and patient[1]:
        try:
            msg = Message("تم تأكيد موعدك في المركز الطبي التخصصي", recipients=[patient[1]])
            msg.body = f"عزيزي/عزيزتي {patient[0]}،\nتم تأكيد موعدك. نتمنى لك دوام الصحة."
            mail.send(msg)
        except:
            pass
    flash('تمت الموافقة وإرسال إشعار', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add_doctor', methods=['POST'])
def add_doctor():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    data = request.form
    conn = sqlite3.connect('medical_center.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, role, name, specialty, email, phone, whatsapp) VALUES (?,?,?,?,?,?,?,?)",
                  (data['username'], data['password'], 'doctor', data['name'], data['specialty'], data['email'], data['phone'], data['whatsapp']))
        conn.commit()
        flash('تم إضافة الطبيب بنجاح', 'success')
    except:
        flash('اسم المستخدم موجود مسبقاً', 'danger')
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/settings', methods=['POST'])
def update_settings():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    data = {
        'google_client_id': request.form.get('google_client_id', ''),
        'google_client_secret': request.form.get('google_client_secret', ''),
        'whatsapp_number': request.form.get('whatsapp_number', ''),
        'smtp_server': request.form.get('smtp_server', ''),
        'smtp_port': request.form.get('smtp_port', ''),
        'smtp_email': request.form.get('smtp_email', ''),
        'smtp_password': request.form.get('smtp_password', ''),
    }
    save_settings(data)
    flash('تم حفظ الإعدادات', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/upload', methods=['POST'])
def upload_file():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    if 'file' not in request.files:
        flash('لم يتم اختيار ملف', 'danger')
        return redirect(url_for('admin_dashboard'))
    file = request.files['file']
    if file.filename == '':
        flash('الملف فارغ', 'danger')
        return redirect(url_for('admin_dashboard'))
    if file and file.filename.endswith('.txt'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        flash('تم رفع الملف بنجاح', 'success')
    else:
        flash('يُسمح فقط بملفات txt', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/download_sample')
def download_sample():
    sample_content = """هذا ملف عينة طبي يحتوي على بعض المعلومات العامة.
يمكن استخدامه لاختبار قدرة الروبوت على التحليل من الملفات.

الصداع النصفي: هو صداع شديد متكرر يصاحبه غثيان وحساسية للضوء. ينصح بالراحة في غرفة مظلمة وتناول أدوية التريبتان.

ارتفاع ضغط الدم: غالباً لا تظهر أعراض واضحة، لكن الصداع والدوخة قد تكون مؤشرات. يجب قياس الضغط بانتظام.

مرض السكري من النوع الثاني: يسبب العطش الشديد، كثرة التبول، والتعب. النظام الغذائي والرياضة أساسيان للعلاج.

الاكتئاب: ليس مجرد حزن، بل مرض يؤثر على النوم والشهية والتركيز. العلاج النفسي والدوائي فعال.
"""
    return send_file(
        io.BytesIO(sample_content.encode('utf-8')),
        mimetype='text/plain',
        as_attachment=True,
        download_name='sample_medical.txt'
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    # تشغيل الخادم على جميع واجهات الشبكة للوصول من الهاتف
    app.run(debug=True, host='0.0.0.0', port=5000)