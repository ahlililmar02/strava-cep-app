import streamlit as st
import requests

# Your Strava API details
CLIENT_ID = st.secrets["strava"]["client_id"]
CLIENT_SECRET = st.secrets["strava"]["client_secret"]
REDIRECT_URI = st.secrets["strava"]["redirect_uri"]


# Step 1: Create the authorization URL
AUTH_URL = f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=activity:read_all"

# Step 2: Check if the 'code' is in the URL (after authorization)
params = st.experimental_get_query_params()

if 'code' in params:
    # User has authorized the app and we received the code
    auth_code = params['code'][0]
    st.write(f"Authorization Code: {auth_code}")

    # Step 3: Exchange the authorization code for an access token
    response = requests.post(
        'https://www.strava.com/oauth/token',
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': auth_code,
            'grant_type': 'authorization_code'
        }
    )

    token_info = response.json()
    if 'access_token' in token_info:
        st.write(f"Access Token: {token_info['access_token']}")
    else:
        st.write("Error getting access token.")

else:
    # Step 4: Display authorization link
    st.write("Click the button below to authorize the app with Strava:")
    st.markdown(f"[Authorize Strava App]({AUTH_URL})")
