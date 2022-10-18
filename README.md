Capstone1- Teacher Gradebook
https://kool-capstone-project-1.herokuapp.com/


The idea for this project came from my experience as a middle and high school teacher and a need that I saw in available gradebook softwares working in that position. Typically, if a student failed an assignment and wanted to redo it, they would have to reach out to their teacher and discuss this. While that sounds like an easy solution, it can be intimidating for some students to the point where they would simply rather not ask. Also, it can be common for an email from a student to be vaugue, resulting in the teacher to have to somewhat blidnly search for whatever assignment the student may be referring to, potentially leading to the teacher having to reach out to the student for more clarification, and ultimately wait for another response before finally resetting the assignment. The goal of the website will be to make a more clear view and communication system for students to see their missing or failed assignments and request another attempt. 

My site has a separate login/ registration page for teachers and students, as they are different views. Both teachers and students can create new accounts and log in to and log out of existing accounts. Once logged in, the student dashboard shows a table with all assignments listed- including the assignment name, due date, score, and potentially an option to request another attempt on an assignment. This will only be available for assignments not marked as "passed" by the teacher. If a student does request another attempt, a message will appear letting them know the request had been sent. 

As for the teacher view, when logged in, the teacher dashboard will be displayed. If a teacher has student requests to reattempt an assignment, they will show at the top of the page with the format "'student name' requests another attempt on 'assignment name'". This can be handled or dismissed. Teachers can edit exiting assignment info- including the assignment name, due date, and students that it is assigned to. Teachers can also select the trash icon to delete a particular assignment. Teachers will also see a button to create a new assignment at the bottom of the page. If a teacher clicks on the assignment name link they will be taken to a view of all student scores on that assignment, and have to ability to edit individual scores.

The seed file contains exisitngs students and teacher to use app with hypothetical class. 


Tech stack: Python, Flask, WTForms, PostgreSQL, SQLAlchemy, Heroku, Jinja, RESTful API(https://dashboard.pusher.com/), JavaScript, HTML, Bootstrap, Bcrypt

