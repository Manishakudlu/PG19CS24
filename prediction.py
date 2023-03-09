# prediction section######

@app.route('/prediction')
def prediction():
    return render_template('user/prediction.html')

@app.route('/prediction1', methods=['post'])
def prediction1():
    os = request.form['textfield']
    alg = request.form['textfield2']
    pc = request.form['textfield3']
    se = request.form['textfield4']
    cn = request.form['textfield5']
    es = request.form['textfield6']
    ca = request.form['textfield7']
    maths = request.form['textfield8']
    cskill = request.form['textfield9']
    hw = request.form['textfield13']
    hk = request.form['textfield12']
    csk = request.form['textfield11']
    psp = request.form['textfield10']
    cts = request.form['RadioGroup14']
    sc = request.form['RadioGroup13']
    tt = request.form['RadioGroup12']
    ods = request.form['RadioGroup11']
    rws = request.form['RadioGroup10']
    mcs = request.form['RadioGroup9']
    ica = request.form['RadioGroup15']
    jh = request.form['RadioGroup8']
    tcs = request.form['RadioGroup7']
    sre = request.form['RadioGroup6']
    mt = request.form['RadioGroup5']
    sw = request.form['RadioGroup4']
    hs = request.form['RadioGroup3']
    wte = request.form['RadioGroup2']
    intro = request.form['RadioGroup1']

    import numpy as np

    ar = []

    ar.append(int(os))
    ar.append(int(alg))
    ar.append(int(pc))
    ar.append(int(se))
    ar.append(int(cn))
    ar.append(int(es))
    ar.append(int(ca))
    ar.append(int(maths))
    ar.append(int(cskill))
    ar.append(int(hw))
    ar.append(int(hk))
    ar.append(int(csk))
    ar.append(int(psp))
    ar.append(int(cts))
    ar.append(int(sc))
    ar.append(int(tt))
    ar.append(int(ods))
    ar.append(int(rws))
    ar.append(int(mcs))
    ar.append(int(ica))
    ar.append(int(jh))
    ar.append(int(tcs))
    ar.append(int(sre))
    ar.append(int(mt))
    ar.append(int(sw))
    ar.append(int(hs))
    ar.append(int(wte))
    ar.append(int(intro))

    aatest = np.array([ar])
    import pandas as pd
    a = pd.read_csv(static_path + "dataset\\career_choices.csv")
    attributes = a.values[:, 0:28]
    labels = a.values[:, 28]

    rf = RandomForestClassifier()
    rf.fit(attributes, labels)
    res = rf.predict(aatest)
    print(res)
    job_roles=['Database Developer', 'Portal Administrator', 'System security Administrator', 'Business System Analyst', 'Software System Engineer',
               'Business intelligence analyst', 'CRM technical developer', 'Mobile Applcation developer', 'UX Designer', 'Quality Assurance associate',
               'Web developer', 'Information Security Analyst', 'Technical support', 'CRM business analyst', 'Project Manager', 'Information technology manager',
               'Programmer analyst', 'Design and UX', 'Sollutions Architect', 'System analyst', 'Network Security administrator', 'Data Architect',
               'Software Developer', 'E-commerce analystTechnical Service', 'Technical Service', 'Information Technology auditor', 'Network security Engineer',
               'Database Manager', 'Application Developer', 'Network engineer', 'Technical Engineer', 'Software quality assurance(QA)/Testing',
               'Database Administrator']
    idx=res[0]
    data=job_roles[idx]
    print(idx, data)
    return render_template('user/prediction.html', data=data)
    # return render_template('user/prediction.html', data=res[0])

