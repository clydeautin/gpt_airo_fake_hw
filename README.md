## Email classifier for customer messages
This email classifier script uses a system prompt and the open AI api to identify and classify inbound customer messages

### Approach
The script can load messages for a seperate location using "load_messages_from_file" method
A prompt is sent with the customer message. The prompt is defined to give the elements exact instructions on how to return
- Categories & action mapping: Giving insights on what the message content is and what should be done about it
- Confidence scoring: Gives us a metric on how confident the LLM is in it's interpretation of the message
Prompt output is ambiguous here as we want to make sure the response is consistent in a json format which is then easier for us to work with
As the prompt is sent we currently use the gpt-40-mini model for cost efficiency and because we don't need a high level model. Temperature is also set at 0.5 to AI hallucinations and keep results consistent

### Tradeoffs

- Message ID: I decided it was important to keep message ID in the JSON response so that we can relate the api response to the customer support message. An easier way to handle this would've been to send the whole json object to the LLM and ask it to send back the message ID in the json output, however, past experience has shown that it is best to avoid any workflow where we ask the llm to send back an exact input so instead msg id is attached as we return the seperately
- Temperature: temperature is set at 0.5 which can be high considering we want consistent results but since we want the LLM to share reasoning on decisions I decided it would benefit from a little bit of a higher temperature
- Loading messages from file was not necessary, I could've simply added the tests messages directly but I figured it would make the script more future proof by including a load_messages_from_file function

### Next Steps

The immediate next step would be more testing, for each of the following categories:
- Can the app sort into all categories
- Can the app score confidence levels accurately

As a team we would want to nail down the exact action categories the LLM would triage into, a set list would help make the results more useful downstream

A lot of the portions of the system prompt are hard coded and instead we could use keyword arguments for things like Confidence Scoring