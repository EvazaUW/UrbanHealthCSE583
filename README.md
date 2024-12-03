# UrbanHealthCSE583

Urban health index analysis and visualization for policy makers at urban and community scale, first phase tool development for a urban health research, jointly developpped as CSE583 course Project.

# Member

- Eva
- Aishwarya
- Sam
- Jingheng

# Docs:

- Project Design Doc: SystemDesign.md (to transform from DocumentationDraft.docx)
  · Idea and Background
  · User Story and Use Cases
  · Componennt Design
  · Tech review (to add tables for pros and cons)
  · Schedule of development (milestones)
  · Chanllenges and Highlights (tech and management)
- Tech review (presentation):
- Tech implementation (Core details)


# Project Structure:
- Backend: 
-   App.py is the main function
-   function_ct.py is the census tract level functions
-   data_preprocessing is the city level functions
- Fontend: urban-health-consultant-v0-frontend
-   src: 
-     - App.js shows the routings (../public/index.html and index.js shows the root created for the react app)
-     - Ubder the components folder --> The three pages (landing page, city level annalysis, census tract level analysis) each

# To run the app:
- run the backend first using: flask --app backend/app run
-   Note that you'll need to have all packages installed to run successfully (install flask, etc)
- run the frontend:
-   first change to the frontent directory: cd urban-health-consultant-v0-frontend
-   (If it the first time you run the frontend, you should use "npm install" here)
-   then use: npm start
-   The frontend should run succesfully
