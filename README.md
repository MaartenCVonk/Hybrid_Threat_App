# Hybrid_Threat_App
Streamlit Application for Hybrid Threat

This app contains the app for hybrid threat deterrence, which has been deployed at a private repository on streamlit: https://hcss-data-lab-hybrid-threat-app-app-ogo1h2.streamlitapp.com/

The structure of the repository is as follows:
├── src
│   ├── cyber.py
│   ├── information.py
│   ├── LP.py
│   └── testing.py
├── app.py
├── Dockerfile
├── requirement.txt
└── README.md

While the app.py is the mainfile that is deployed, it sources the frontend from the cyber.py and the information.py in the src folder. The calculations is sourced from the LP.py. The testing.py is used for testing purposes.
The dockerfile contains all the relevant components for deployment, from which some are sourced from the requirement.txt.
