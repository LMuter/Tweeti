
# Load Messages

To access the upload page, there is no dedicated button in the admin interface. Instead, you must use a direct URL to navigate to the upload page. Uploading a file requires a CSV file with at least two mandatory columns: `id_str` and `full_text`. The `id_str` column contains a unique identifier that links each Tweeti entry to the original items from the uploaded dataset (since every entry in Tweeti will receive its own numeric ID when the CSV file is loaded). The `full_text` column should contain the main content of the message (e.g., a tweet or post), which may include text, hashtags, emojis, and URLs.


## Upload Data Files

To upload a data file, ensure your Tweeti instance is running at `<your url>` (e.g., `https://www.example.com`). Navigate to `<your url>/upload` (e.g.,`https://www.example.com/upload`) to access the upload page, as shown in Figure \ref{fig:fileupload}. On this page, you can select a data file and optionally provide a description that will be visible on the admin page. Once you click the "Upload" button, the file will be uploaded to Tweeti.

![File upload page to load a CSV file in Tweeti. \label{fig:fileupload}](resources/images/upload.png){ width=250px }

### File Requirements

To ensure the file is processed correctly, it must meet the following requirements:

- The file must be in CSV format (comma-separated values).
- The file encoding should be UTF-8.
- The first row must contain headers, with at least `id_str` and `full_text` headers present (additional headers are allowed and will be stored under content).
- Each subsequent row must have values for the `id_str` and `full_text` columns.
- Optionally, a column can be included for URLs, which can link to the original resource of the message. This URL will be displayed to labelers, allowing them to access the original message for additional context.


## Example

Below is an example of the content of a suitable CSV file (this could be exported from Excel with a comma , as the delimiter):

```
Id, id_str, full_text,                url
0,  1234,   this is a message,        url_to_original_resource
1,  2345,   this is also a message,   url_to_original_resource
2,  3456,   this is another message,  url_to_original_resource
```



\newpage{}
