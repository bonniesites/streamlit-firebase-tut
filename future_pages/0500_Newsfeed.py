import streamlit as st

from mods.data_processing import *

# Set up MongoDB connection
CONN = MongoClient('localhost:27017')
# CONN = MongoClient(st.secrets.mongo.conn_string)


# Mock data for demonstration
data = {
    'Title': ['Article 1', 'Article 2', 'Article 3'],
    'Link': ['https://example.com/article1', 'https://example.com/article2', 'https://example.com/article3'],
    'Date': ['2024-03-20', '2024-03-19', '2024-03-18'],
    'Summary': ['Summary of article 1...', 'Summary of article 2...', 'Summary of article 3...'],
    'Hero Image': ['https://example.com/image1.jpg', 'https://example.com/image2.jpg', 'https://example.com/image3.jpg'],
    'Author': ['Author 1', 'Author 2', 'Author 3'],
    'Category': ['Category 1', 'Category 2', 'Category 1']
}

URLS = [
    'https://cyware.com/hacker-news'
    ,'https://www.bleepingcomputer.com/news/security/'
    ,'https://therecord.media/'
    ,'https://es.wired.com/tag/ciberseguridad'
    ,'https://cyware.com/cyber-security-news-articles'
    ,''
    ,''
]

TOOLS = [
    ''
    ,''
]


###########################
##   *** Functions ***   ##
###########################

# Function to fetch news articles using News API
def fetch_news_from_api(keyword):
    api_key = st.secrets.NEWS
    url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['articles']
    else:
        st.error("Failed to fetch news articles from API")

# Function to scrape news articles from a website
def scrape_news_from_website(keyword):
    for url in URLS:
        url = f"{url}={keyword}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Write your scraping logic here to extract news articles
            articles = []
            return articles
        else:
            st.error("Failed to scrape news articles from website")


# Function to summarize an article using AI
def summarize_article(url):
    article = Article(url)
    article.download()
    article.parse()
    summarizer = pipeline("summarization")
    summary = summarizer(article.text, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Function to search for cybersecurity news articles
def search_cybersecurity_news(query):
    # Placeholder function, you need to implement your own logic to search for news articles
    # For example, you can use news APIs or web scraping techniques
    return []

# Main function to run the Streamlit app
def main():
    st.title("Cybersecurity News")
    
    
    st.title("News Article Search")

    # Sidebar for user input
    keyword = st.sidebar.text_input("Enter keyword to search")

    # Options for fetching news articles
    option = st.sidebar.radio("Select option", ("API", "Web Scraping"))

    # Fetch news articles based on selected option
    if st.button("Search"):
        if option == "API":
            articles = fetch_news_from_api(keyword)
        elif option == "Web Scraping":
            articles = scrape_news_from_website(keyword)

        # Display news articles
        if articles:
            for article in articles:
                st.subheader(article['title'])
                st.write(article['description'])
                st.write(f"Source: {article['source']['name']}")
                st.write(f"Published At: {article['publishedAt']}")
                st.write(f"URL: [{article['url']}]({article['url']})")
                st.markdown("---")
        else:
            st.warning("No articles found")

    # Sidebar for search and sorting options
    st.sidebar.header("Search Articles")
    search_query = st.sidebar.text_input("Search for news", "")
    sort_by = st.sidebar.selectbox("Sort by", ["Date", "Category", "Title"])

    # Fetch news articles based on search query
    articles = search_cybersecurity_news(search_query)

    # Apply sorting based on user selection
    if sort_by == "Date":
        articles.sort(key=lambda x: x['date'], reverse=st.sidebar.checkbox("Sort descending"))
    elif sort_by == "Category":
        articles.sort(key=lambda x: x['category'])
    elif sort_by == "Title":
        articles.sort(key=lambda x: x['title'])

    # Display articles
    for article in articles:
        st.subheader(article['title'])
        st.write(f"Date: {article['date']}")
        st.write(f"Category: {article['category']}")
        st.write(f"Author(s): {[f'[Author Name](link_to_bio)' for author in article['authors']]}")
        st.write(f"Summary: {article['summary']}")
        st.write(f"Link: {article['link']}")
        st.image(article['hero_image'], caption="Hero Image", use_column_width=True)
        
        


# Run the app
if __name__ == "__main__":
    main()