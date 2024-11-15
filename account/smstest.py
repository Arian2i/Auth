import ghasedak_sms
sms_api = ghasedak_sms.Ghasedak(baseurl="http://your_base_url/api/v1", apikey='')
response = sms_api.send_otp_sms(receptor='09353732203', message='Your OTP message')