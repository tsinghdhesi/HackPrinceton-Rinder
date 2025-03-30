###
# Rinder
###

<img src="https://github.com/user-attachments/assets/697a3fd5-fe22-4695-8b54-bd23bbbe8181" alt="logo" width="200"/>

## "Enter your username and find your Reddit soulmate!"

Rinder is a mobile app designed to help Reddit users find their most compatible matches based on their activity on the platform. By analyzing user comments, posts, and voting behaviors using [Gemini](https://gemini.google.com/app), Rinder calculates a similarity score and recommends the top three most compatible Reddit users. To add more depth, we use [Gemini](https://gemini.google.com/app) to generate a description of why each match is a strong contender.

## Features

* Reddit User Analysis: Scrapes Reddit data, including posts and comments.

* Generates a list of likey subreddits that the user is or may be interested in.

* Similarity Scoring: Cross-references user activity and assigns a similarity score to potential matches.

* Top 3 Matches: Identifies and displays the three most compatible Reddit users.

* AI-Powered Explanations: Uses [Gemini](https://gemini.google.com/app) to conduct sentimental analysis and to describe why each match is a good fit.

* Mobile-Friendly UI: Developed with [Flask](https://flask.palletsprojects.com/) for a seamless user experience.

 ## Tech Stack

* Frontend: [Flask](https://flask.palletsprojects.com/)  (HTML and CSS for website integration)

* Backend: Python (for data processing and analysis)

* Web Scraping: Utilizes Reddit API

* AI Integration: Gemini for generating compatibility explanations

## Installation

### Prerequisites

Ensure you have the following installed:

* [Flask](https://flask.palletsprojects.com/)

* Python

### Steps

1. Clone the repository

```sh
git clone https://github.com/yourusername/hackprinceton-rinder.git
cd hackprinceton-rinder
```

2. Install frontend dependencies

```sh
Flask
praw
gemini_ai

```

3. Run the server

```sh
python app.py
```

## Usage

1. Open the app and enter your Reddit username.

2. The app retrieves your activity from Reddit and processes your data.

3. Based on the similarity score, you receive three potential Reddit soulmates.

4. Read the AI-generated descriptions of why you match with them.

5. Connect (with the help of AI generated prompts) and start engaging with like-minded Redditors!

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.

2. Create a new branch (git checkout -b feature-branch).

3. Commit your changes (git commit -m "Add new feature").

4. Push to the branch (git push origin feature-branch).

5. Create a pull request.

## License

This project is licensed under the [MIT License](LICENSE) - see the [MIT License](LICENSE) file for details.

## Contact

For any issues or suggestions, please open an issue in the repository or reach out at tsinghdhesi@colgate.edu, jwu5@colgate.edu, wguo@colgate.edu, or yheleveria@colgate.edu.
