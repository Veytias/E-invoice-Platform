# Seng2021-Project
Invoice Receiving
Invoices may also be exchanged between different systems. Therefore, to better manage invoices, the system needs a component that can receive invoices from the external environment. This category of service should be able to retrieve e-invoices from a developer-designated media, which can possibly be API calls, email, SFTP, chatbot, or even SMS. Your service should be able to detect the new invoices.

Input
Input should conform to the UBL format in the recommended format. (i.e., The input should be able to pass the validator mentioned in the “Invoice Validation” section). But you should consider and define how your service takes the input. You should design an asynchronous mechanism to get information. A simple upload HTTP API without any validation is acceptable as a start, but not sufficient for the service.

Output
The observable output of this service includes a report. After the API call, your service should return a communication report. The format of the report can be but not limited to JSON, HTML, PDF. In a successful execution, the service should persist the invoice. If there is any communication error, it is preferable that your service reacts with a human-readable message.


# To run app:
