# Documentation
This directory documents ideaHub's development to best serve the "long tail" in Agile methodology

## Database
See database.md for information on data structure and services

## Tech Stack
See techstack.md for a comprehensive list of the "tech stack" of ideaHub

## Server information
This application was made using Google Cloud Platform (GCP), specifically Google App Engine.  By using this platform, we are able to serve dynamic content to any user.  We also gain access to Google Cloud Datastore, GCP's provided database system.  Managing this requires specific permissions form the owner of the GCP project and access to secrete key files, which are hidden for the purposes of security.  GCP is free to use to an extent, though academic credit is available with the right connections.

## Future Improvements
- Make layouts more responsive, specifically for mobile using Javascript
- Enchance style and design by adding animations and other geometries
	- Revisit current style upon usability report
- Modify databse so that User's can do the following:
  - save progress between sessions on working applications/ideas
  - edit existing applications/ideas
  - upload image files directly as opposed to url format
  - view previous applications/ideas based on recent activity
- Upgrade security to use HTTPS

## Known "Bugs"
- Security requires further attention
- On small viewports, navigation mention becomes impossible to use
- "Apply" not currently linked up to submit a real application
	- Currently, this page is only a placeholder for the purposes of demonstration.  Future plans are to email or have in-house application management
- Stasis theory missing "Definition" due to limits on entity size in GCP
- Multiple ideas with the same title can exist leading to undefined behavior in fetching ideas from databse