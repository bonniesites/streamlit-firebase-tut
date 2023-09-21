PAGE_HEADER = 'Trig Functions'
PAGE_HEADER = ''
SIDEBAR = 'collapsed'
MENU_ITEMS = {
       'Get Help': 'https://my-reddit.streamlit.app/',
       'Report a bug': 'https://my-reddit.streamlit.app/',
       'About': '# This is a header. '
}

from mods.base import *




trig_funcs = {}
for theta in unit_circle:
    radians = np.deg2rad(theta)
    radians_pi = create_rad_symbol(theta)
    hyp = radius
    opp_angle = theta 
    right_angle = 90
    adj_angle = 90 - theta
      
    # st.subheader(f'radians: {radians}')    
    # st.subheader(f'np.sin(radians): {np.sin(radians)}')

    xcos = np.cos(radians)        
    ysin = np.sin(radians)
    tan = calc_trig_function(ysin, xcos)
    sec = calc_trig_function(1, xcos)
    csc = calc_trig_function(1, ysin)
    cot = calc_trig_function(1, tan)
    if theta == 0.0:
        ysin = 0.0
    if theta == 90 or theta == 270:
        tan = 'undefined'
        sec = 'undefined'
    if theta == 180 or theta == 360:
        cot = 'undefined'
        csc = 'undefined'
    
    cos_sym = convert_to_symbols(xcos)
    sin_sym = convert_to_symbols(ysin)
    tan_sym = convert_to_symbols(tan)
    sec_sym = convert_to_symbols(sec)
    csc_sym = convert_to_symbols(csc)
    cot_sym = convert_to_symbols(cot)
    
    new_angle = {
        'theta': theta,
        'radians': radians_pi,
        'cos': xcos,
        'sin': ysin,
        'tan': tan,
        'sec': sec,
        'csc': csc,
        'cot': cot,
        'cos_sym': cos_sym,
        'sin_sym': sin_sym,
        'tan_sym': tan_sym,
        'sec_sym': sec_sym,
        'csc_sym': csc_sym,
        'cot_sym': cot_sym
        } 
    
    trig_funcs[theta] = new_angle
        

with st.container():
    st.subheader('Unit Circle Values')
    # Unit Circle Calculations
    deg_col, rad_col, cos_col, sin_col, tan_col, sec_col, csc_col, cot_col = st.columns(8)

    with deg_col:
        'Degrees'    
    with rad_col:
        'Radians'       
    with sin_col:
        'Sine'           
    with cos_col:
        'Cosine'      
    with tan_col:
        'Tangent'       
    with csc_col:
        'Cosecant'       
    with sec_col:
        'Secant'          
    with cot_col:
        'Cotangent'
    for degree, angle_data in trig_funcs.items():
            # Display
            with deg_col:
                st.write(str(degree))
            with rad_col:
                st.write(angle_data["radians"])
            # Sine
            with sin_col:              
                st.write(angle_data['sin_sym'])
            # Cosine
            with cos_col:                
                st.write(angle_data['cos_sym'])             
            # Tangent
            with tan_col:                
                st.write(angle_data['tan_sym'])
            # Cosecant
            with csc_col:                
                st.write(angle_data['csc_sym'])     
            # Secant
            with sec_col:                
                st.write(angle_data['sec_sym'])        
            # Cotangent
            with cot_col:                
                st.write(angle_data['cot_sym'])
                    


    # for degree, angle_data in trig_funcs.items():
    #     #pass    
    #     st.write(f'{degree}')
    #     st.write(f'{angle_data["radians"]}')
    #     st.write(f'{angle_data["cos"]}')
    #     st.write(f'Sine: {angle_data["sin"]}')
    #     st.write(f'Tangent: {angle_data["tan"]}')
    #     st.write(f'Secant: {angle_data["sec"]}')
    #     st.write(f'Cosecant: {angle_data["csc"]}')
    #     st.write(f'Cotangent: {angle_data["cot"]}')
    #     st.write(f'Cosine Symbolic: {angle_data["cos_sym"]}')
    #     st.write(f'Sine Symbolic: {angle_data["sin_sym"]}')
    #     st.write(f'Tangent Symbolic: {angle_data["tan_sym"]}')
    #     st.write(f'Secant Symbolic: {angle_data["sec_sym"]}')
    #     st.write(f'Cosecant Symbolic: {angle_data["csc_sym"]}')
    #     st.write(f'Cotangent Symbolic: {angle_data["cot_sym"]}')
    #     st.write('-' * 40)
    
    
    
    
    
    
    textkey = "{\n  \"type\": \"service_account\",\n  \"project_id\": \"streamlit-reddit-5b36c\",\n  \"private_key_id\": \"638c7f8fe5545d8143e1d96e109196a4423d54e0\",\n  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDXNMvpxw6NJzgd\\n3eo/rZb/8x3dDaSJKS9XGL+rj3A9wWa1TZ6WHf2P1o2wjx/MKl/mr4ogWbtbjhvs\\nwIWyb8HCJ3A5F2pQsvp7eVt4UZm50wXBL+qLMXVTfuLnrT0NOgh0rDvPdOufvjtd\\nTfpU6QRutCUDfjz0ywkRZQHZyT+J27CV2izM/EnXLNLNHVn4Y8cruaf4ytMJpX+E\\nhMiHrxss4cTNZK7uOChv3aU41YxBOlqEMvhP9fIYr5diqs1GjHfBDdUVf1pQDVrQ\\nHWkg+LEtb1FjuSii0HkZ335fn5rUE/X2g9IgRR/z2KnSVBsSHZtFzI7sZjEIeG0Q\\nGGgmtDGhAgMBAAECggEAEiI0gXcgsoOovpmFpMZ5iAkiDc+ZuuYBw27GLcxZGpcK\\nksHe2ErgJAfh6gvxU7iJWqyVcLrm5uTPVRB24413r+a3VdQzhOfD4/Yan0WO9MHD\\nhR8GviJVfsrdD0UBdTUb48rkgktZlF0I7wiETLXSxgo/aS8wrzbRhYnzkTicNj8p\\nX+JgGSPYSkf5gRauDSOQEnkRi/T9YtB23pyc7BlhMHwHeExQmqy7eu76w3jxvNtE\\nbPmaqWxT87raWgjRKyQvlHd2/BaWS7m+oPhLdck/ntcp/xFL4H9zD2/EbTxmbO6W\\npEuLaNUfEu4Ymu/99AOqRep5KFZlNYLQz0st3Cp1jQKBgQD4gw2cnKmg0GRHgPrY\\nZIlHebx5gz7VE383ol7ji2DXeT1yPgoZwS0sM626b98efHJnSITA8/w6JM37hLfO\\nbfSSiuPaSeghQBrhkGdYr4awKZQBH4EjED1jkN0jxNIhzFYdMLobHnHWGQBw+hPn\\nd3gdh4rtAG0G5il/1a6B1KgFzQKBgQDdsNVNcbmW8+FYDrC/uo6c2k1hOEt1Hz29\\nr9m6EkzWUJ9yCI4UTSo5LS5ALbNH/BAJApbhWjzN44yVq/2gDsH6Y9v2KDLr3KN/\\ngkLy/ZNc4XgXjGVooyrJpw6fNtn1cIKETWNHDvdk4Q9uxN5hPj/oXNXbyQRYpZ2v\\nfGeZDI3HJQKBgDFdBuUnEWLKQkEZ07oMLmCuQ8v3UBHPL6QDcsnMM85ZXOVGgYcg\\nIjL3iPjRpAZQPgFaHFSfomiCSxA9Cq3MlZpOUHhZ2exQ6YYIwx6QrzZq6+VVNrea\\nUDdo3SRvwjXIewqNVUpxv7cBfF70reN6jbd/5w6w2PdX3MJx1Zogfce5AoGAcah3\\ns3za6cmffsYJWEMNWt2RTobOKP4baWT++6bmPfqXxJ8eOMpXG3lOfRjxEbbpgbUS\\nJfddtTE0oofLQIRQb09DNrDlaod0S6s9J9dZ9gSizW/tjfgZt8kudfJpTKyiPbJv\\nc774l3/Lqb7FRJXlrfvqqQQmdkxyy8W8V3tYNQECgYA/BEkFIBRPdcctyL/GoH4J\\nwP9yTdY/HWEotRytP7IiK+zrbecEEKV4W7lcZCuKPIG6KyA1VJpaS7ma6MiTxz/Q\\nwhoRGjkwYa2mkjxDE9v6lZuLh7/c3r7VV2NTS+mjheorp+XwdWxsoTuapnkbAqM0\\nWnYv1kPivm6b+2MlLx9sIQ==\\n-----END PRIVATE KEY-----\\n\",\n  \"client_email\": \"firebase-adminsdk-wlg6r@streamlit-reddit-5b36c.iam.gserviceaccount.com\",\n  \"client_id\": \"101266216680740215397\",\n  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-wlg6r%40streamlit-reddit-5b36c.iam.gserviceaccount.com\",\n  \"universe_domain\": \"googleapis.com\"\n}\n"
