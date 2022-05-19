# Resume-Coding-Examples
Examples of previous coding projects documenting problem identification skills as well as coding literacy
 

## UCSDCoursesScraper
- Most recent and most ambitious python automation process to date
- Incorporates Python's “Selenium” package to log in to and web-scrape our school's course enrollment tool to retrieve a student's course info. Then uses the "googleapiclient" package to create a custom color-coordinated calendar with descriptive events for each of the student's courses.
- Incorporates other “base” packages like “re” (regular expression), “pickle” (serialize package), “sys” (for custom error throwing and handling), and “pprint” (used for debugging unwieldy outputs).
- Written to avoid problems I'd encounter previously with my "LAB_HOURS" program maxing out Google's free API calls
- Automates what would usually amount to multiple hours of busywork into a few minutes.
- Have received significant interest from other UCSD students to purchase my code (I haven’t been able to though due to legal issues concerning the data my code handles).
 
 
## LAB_HOURS
- Written to document the number of hours that robotics team members spent in the school robotics room. This was necessary for determining who “deserved” to go to regionals and world championships if our budget did not cover our entire team's tickets (which it most often did not).
- Built using the “gspread” Google sheets python package and the "oauth2client" package to read and edit Google sheets.
- Contains a built-in installer for the packages used within it making it easy to quick on multiple devices.
- At this point, I had some familiarity with python through other small side projects (e.g., creating a python server and client to create an encrypted chat room).
- My program saw usage and success for about half the robotics team’s season before ceasing to function after hitting the free limit on Google’s API calls due to the amount of data it was accessing and storing.
 
 
## Sorba 2.0
- First-ever attempt at writing a program to automate a repetitive web-based task. Basically, just a rudimentary macro.
- Built using the “pyautogui” python package
- Written to take any Spanish words I wasn't familiar with on my screen, plugging them into a translator, and creating flashcards of them on an online tool called Quizlet (required by my Spanish class at the time).
- Wherein the macro-less process took ~45 seconds per word to do manually, my finalized program made each word take as little as 3 seconds.
- This was later used to successfully document to our Spanish teacher that the texts we were given exceeded our current Spanish proficiency.
- Despite its crude nature, I received multiple monetary offers from my peers to adapt my code to run on their computers.
