# CampusCare – Campus IT Helpdesk and Issue Tracking System

## 1. Abstract
CampusCare is a web-based helpdesk application for reporting and tracking campus IT problems. Students can submit an issue with their name, email, category and description. The system creates a ticket number that can be used with the registered email address to check progress. An administrator can review tickets and update their status and priority.

## 2. Problem statement
Campus IT complaints are often communicated informally, making it difficult for students to know whether an issue has been received or resolved. CampusCare provides a central place to record requests and monitor their progress.

## 3. Objectives
- Provide a simple online form for reporting campus IT issues.
- Store support requests in a structured SQLite database.
- Allow a student to look up a ticket using its ID and email.
- Allow an administrator to update ticket status and priority.
- Demonstrate software delivery practices using Git, Jenkins and Docker.

## 4. Modules
1. Home dashboard – displays total, pending, in-progress and resolved ticket counts.
2. Ticket submission – validates and stores student issue details.
3. Ticket tracking – retrieves a ticket only when its ID and email match.
4. Admin authentication – requires an admin password before the admin dashboard is accessible.
5. Admin ticket management – updates ticket status and priority.

## 5. Technology stack
- Frontend: HTML and CSS
- Backend: Python and Flask
- Database: SQLite
- Version control: Git and GitHub
- CI: Jenkins
- Containerization: Docker

## 6. Architecture
Browser → Flask routes → SQLite database. Jenkins checks out the Git repository, installs Python dependencies, runs automated tests and builds a Docker image. Docker runs the web application in a container and stores the SQLite database in a persistent volume.

## 7. Ticket workflow
Pending → In Progress → Resolved. The administrator may also adjust priority to Low, Medium or High.

## 8. Testing
Automated tests cover homepage loading, ticket submission, ticket lookup, protection against lookup with the wrong email, admin login protection and ticket status updates. Run them with:

```bash
python -m unittest discover -s tests -v
```

## 9. DevOps workflow
1. Track source changes with Git.
2. Push the repository to GitHub.
3. Configure Jenkins to build the repository using the included Jenkinsfile.
4. Jenkins installs requirements and executes the automated test suite.
5. Jenkins builds the Docker image when the preceding stages pass.
6. Run the image locally or through Docker Compose.

## 10. Limitations and future enhancements
This is an academic demonstration application. The admin password is a single shared credential; a real deployment should use individual staff accounts, password hashing, CSRF protection, HTTPS, audit logging, backups and a production database. Email notifications and file attachments can be added later.

## 11. Conclusion
CampusCare demonstrates a complete small application and a repeatable build-and-test workflow. It combines a practical campus support use case with version control, automated testing, CI and containerization.
