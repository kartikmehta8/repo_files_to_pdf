import requests
import markdown
from weasyprint import HTML

def traverse_repo(api_url, headers, path=''):
    contents_url = f"{api_url}/contents/{path}"
    response = requests.get(contents_url, headers=headers)
    response.raise_for_status()
    contents = response.json()
    markdown_content = ""
    for content_file in contents:
        if content_file['type'] == 'dir':
            print(f"Entering directory: {content_file['path']}")
            markdown_content += traverse_repo(api_url, headers, content_file['path'])
        elif content_file['name'].endswith(('.md', '.mdx')):
            print(f"Parsing file: {content_file['path']}")
            file_response = requests.get(content_file['download_url'], headers=headers)
            file_response.raise_for_status()
            markdown_content += file_response.text + "\n\n"
            print(f"Saved content from: {content_file['path']}")
    return markdown_content

def markdown_to_pdf(markdown_content, pdf_filename):
    print(f"Converting Markdown content to PDF: {pdf_filename}")
    html_content = markdown.markdown(markdown_content)
    HTML(string=html_content).write_pdf(pdf_filename)
    print(f"PDF file created: {pdf_filename}")

def run_bot():
    repo_link = input("Enter the GitHub repository link: ")
    pdf_filename = input("Enter the name of the PDF file: ")
    token = input("Enter your GitHub token: ")

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    repo_api_url = repo_link.replace('https://github.com/', 'https://api.github.com/repos/')
    print("Starting to traverse the repository...")
    markdown_content = traverse_repo(repo_api_url, headers)
    markdown_to_pdf(markdown_content, pdf_filename)

if __name__ == "__main__":
    run_bot()
