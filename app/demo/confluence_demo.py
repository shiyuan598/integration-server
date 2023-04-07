import requests
import json # loads / dumps

headers = {
    'Content-Type': 'application/json',
}
response = requests.get(
    'https://confluence.zhito.com:8090/rest/api/space/ITD',
    headers=headers,
    auth=("wangshiyuan", "zhito26@#"))
print(response, response.text)

response = requests.get(
    'https://confluence.zhito.com:8090/rest/api/content/56102841',
    headers=headers,
    auth=("wangshiyuan", "zhito26@#"))
print("\n\n", response, response.text) # _links.webui


# 1. Install the Atlassian Python API library (called "atlassian-python-api") using pip. 

# ```
# pip install atlassian-python-api
# ```

# 2. Create an instance of the Confluence class from the API.

# ```python
# from atlassian import Confluence

# confluence = Confluence(
#     url='https://your-confluence-url.com/',
#     username='your-username',
#     password='your-password'
# )
# ```

# 3. Use the `create_page()` function to create a new page in Confluence.

# ```python
# result = confluence.create_page(
#     space = 'your-space-key',
#     title = 'Your Page Title',
#     body = 'Your page content in Confluence Storage Format (CSF), e.g. <p>This is some text</p>',
#     parent_id = 12345678  # ID of the parent page (optional)
# )
# ```

# 4. If you want to update an existing page, use the `update_page()` function instead.

# ```python
# result = confluence.update_page(
#     page_id = 12345678,
#     title = 'Your Updated Page Title',
#     body = 'Your updated page content in CSF'
# )
# ```

# 5. To delete a page, use the `delete_page()` function.

# ```python
# confluence.delete_page(page_id=12345678)
# ```

# That's it! With these few lines of Python code, you can start creating and updating pages in Confluence. Remember to format your page content in Confluence Storage Format (CSF) to ensure correct rendering of elements like headings, bullet points, and tables.