# Brevium-Interview

For the project, I split my 3 hours into the following sections:
15 minutes - Gathering requirements, thinking of stakeholder questions, understanding impact
30 minutes - API discovery
15 minutes - Design the program based on my understanding of the project scope
90 minutes - Code up the project
30 minutes - Comment the code, and write test cases

# Gathering Requirements, Stakeholder Questions, Understanding Impact

End goal:
Create a program that is able to schedule in appointments using the existing API

Scope:
Running on the assumption that it is a program that will run daily

Metric:
Considered a success when all the appointments have been scheduled in and there are no overlaps and it won't run into failure

# API Discovery

GET /Schedule -- returns the inital schedule of the doctors
POST /Schedule -- send with header and will "update the schedule" with a new time slot being taken up
GET /AppointmentRequest -- grabs the next appointment request in the queue and will return a 204 when there is nothing left on the queue
POST /Start -- turns on the system and resets the system
POST /Stop -- debugging and testing purpose

# Program Design

Will always need to start with POST /Start to run tests and debug
GET /Schedule to get the schedule for the month
GET /AppointmentRequest to find the next appointment on the queue to enter into the schedule
If the appointment meets the requirements, schedule them in
POST /Schedule to mark the time slot as take
POST /Stop once everything is done to see if the schedule is correct
