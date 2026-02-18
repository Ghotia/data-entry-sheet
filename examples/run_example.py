from phishing_detector import analyze_url, analyze_email, make_alert

sample_url = 'http://paypal.com.user.verify.verify-login.info'
analysis = analyze_url(sample_url)
print('URL analysis:', analysis)

if analysis['suspicion_score'] >= 0.6:
    alert = make_alert(
        vector='url',
        target='user@example.com',
        threat_type='URL-based phishing (heuristic)',
        risk_score=analysis['suspicion_score'],
        analysis={'technique_detected': 'heuristic_url', 'features_used': list(analysis['heuristics'].keys())},
        actions=['simulated_block']
    )
    print('Generated alert:')
    print(alert)

# Example email
headers = {'From': '"PayPal Support" <no-reply@paypal.com.user.verify.verify-login.info>'}
body = 'Your account will be suspended unless you verify now: http://paypal.com.user.verify.verify-login.info/login'
email_analysis = analyze_email(headers, body)
print('Email analysis:', email_analysis)

if email_analysis['suspicion_score'] >= 0.6:
    alert = make_alert(
        vector='email',
        target='user@example.com',
        threat_type='Email phishing (heuristic)',
        risk_score=email_analysis['suspicion_score'],
        analysis={'technique_detected': 'display_name_mismatch/urgent_language', 'features_used': ['display_name_mismatch','urgency_score']},
        actions=['simulated_quarantine']
    )
    print('Generated alert:')
    print(alert)
