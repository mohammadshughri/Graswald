Explanation:

1. Fetches posts from the given API.

2. Analyzes each post, identifying unique words in the title and body, and common words between them.

3. Generates a word cloud for each post using all the words (unique and common).

4. Creates an HTML report with the analysis results and word clouds.

How to Run the Script:
Ensure you have Python installed on your system.
Install the required libraries using pip:

`pip install requests pandas matplotlib wordcloud`

Run the script using Python:

`python task_2.py`

The script will generate a report.html file in the same directory, which you can open in a web browser to view the results. The number of posts analyzed can be changed by modifying the argument in the main(5) call at the end of the script.
