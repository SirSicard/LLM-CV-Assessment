# Evolution, Thoughts, and Conclusions on the CV Evaluation Prompt Design

## Initial Approach

In developing the CV evaluation tool, my primary goal was to create an efficient and accurate system that leverages OpenAI's GPT-4 capabilities to evaluate candidate resumes against specific job titles. The initial challenge involved defining the core functionality: validating inputs, constructing prompts, interacting with the OpenAI API, and processing the output to meet the specified JSON format.

## Evolution of the Prompt Design

### 1. Basic Prompt Construction

Initially, the prompt was simple, focusing on providing the candidate's CV and the job title directly to the language model. The initial version of the prompt was:

Evaluate the following CV for the job offer titled 'Comercial de automóviles'. Provide a JSON response with the following information: 
1. A numerical score (0-100) based on the relevance of experience. 
2. A list of related experiences (Position, Company, Duration). 
3. An explanation describing why the score was assigned.

Job Offer Title: Comercial de automóviles

Candidate CV:
{candidate_cv}

This approach, although straightforward, produced inconsistent results. The model sometimes misinterpreted the scoring criteria or included irrelevant experiences.

### 2. Refinement of Prompt Details

To enhance the clarity of the evaluation criteria, I refined the prompt to include more explicit instructions. The focus was on emphasizing relevance and ensuring the model understood the need for structured JSON output. The updated prompt became:

Evaluate the following CV for the job offer titled '{job_title}'. Provide a JSON response with the following information: 
1. A numerical score (0-100) based solely on the relevance of the candidate's past experiences to the job title. 
2. A list of related experiences with detailed information: Position, Company, Duration. 
3. An explanation of the score with a detailed description of the candidate's related experience.

Ensure the JSON output is well-structured and clearly formatted.

Job Offer Title: {job_title}

Candidate CV:
{candidate_cv}

This version improved the relevance of the results by making the evaluation criteria clearer.

### 3. Optimization for Consistency

The next stage involved optimizing the prompt to ensure consistent and accurate JSON formatting. This involved explicitly requesting the language model to validate its JSON structure before returning the response. The final version incorporated:

- Clear delineation of expected JSON fields.
- Instructions for validating the JSON output.

The refined prompt looked like this:

Evaluate the following CV for the job offer titled '{job_title}'. Provide a JSON response with the following information:
1. A numerical score from 0 to 100 based on how well the candidate's experience matches the job title. Only include experiences directly relevant to the job title.
2. A list of related experiences, including Position, Company, and Duration.
3. A detailed explanation of why the score was assigned, including an analysis of the candidate's relevant experience.

Please ensure the JSON output is correctly formatted and contains all required fields.

Job Offer Title: {job_title}

Candidate CV:
{candidate_cv}

## Challenges Faced and Solutions

### 1. Input Validation

Ensuring that both the job title and CV were of sufficient length and detail was crucial for effective evaluation. I implemented a validation function that checks for a minimum length, which helps in filtering out incomplete or insufficient data.

### 2. Handling Different File Formats

Reading CVs from different file formats (PDF, DOCX) was challenging due to the variability in text extraction methods. I utilized \`PyMuPDF\` for PDFs and \`python-docx\` for DOCX files, implementing robust error handling to manage potential issues during text extraction.

### 3. JSON Parsing and Error Handling

Parsing the JSON response from the LLM was another area where i had issues, particularly with malformed JSON responses. I added error handling to log and manage JSON parsing errors, ensuring that the system could handle unexpected output from the API.

## Conclusions

The iterative process of refining the prompt and the system's functionalities led to a robust tool capable of evaluating CVs effectively. The key takeaways from this development process include:

- **Clarity and Specificity**: Providing clear and specific instructions to the language model significantly improves the relevance and accuracy of the output.
- **Validation and Error Handling**: Implementing rigorous input validation and error handling ensures the system can handle various edge cases and maintain robustness.
- **User Guidance**: Providing users with clear instructions and feedback enhances the overall user experience and ensures the system's effective utilization.

## Potential Improvements

While the current system is fully functional, several areas offer room for enhancement:

1. **Enhanced Scoring Criteria**: Developing a more sophisticated scoring algorithm that considers factors like industry standards, specific skill requirements, and the relevance of education and certifications could improve the accuracy of evaluations.

2. **User Interface Development**: Creating a graphical user interface (GUI) would make the tool more accessible to users unfamiliar with command-line operations, thereby broadening its usability.

3. **Security and Configuration Enhancements**: Adding features to handle environment-based API keys and configuration settings securely could improve the tool’s robustness and adaptability.