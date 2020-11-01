import re
import requests
import bs4
import string
import csv


def get_home_url():
    """
    :return: home url of that site
    """
    input_url = input("Enter the url ")  # input url from user
    h_url = re.findall("https*://[a-zA-Z0-9.]*", input_url)[0]  # to get home url
    return h_url


def get_soup(url):
    """
    :param url:
    :return: soup variable of the given url
    """
    result = requests.get(url)  # to get the site information
    soup = bs4.BeautifulSoup(result.text, "lxml")  # converting the results into soup variable
    return soup


def get_links(soup, url):
    """
    :param soup:
    :param url:
    :return: set of internal links and external links of url:
    """
    internal_links = set()  # to store all internal links of the website
    external_links = set()  # to store all external links of the website
    all_links = soup.select('a')  # to get all anchor tags
    for link in all_links:
        data = link.get('href')  # to get the href content
        if data is not None:  # if there is a href content
            if url in data:  # if url is in link
                internal_links.add(data)
            elif "https://" not in data and "http://" not in data:  # if referenced to the same page, with out url
                internal_links.add(data)
            else:  # if it's an external link
                external_links.add(data)
        else:  # if there is no href content
            internal_links.add(data)
    return internal_links, external_links


def get_text_list_format(soup):
    """
    :param soup:
    :return: list of all text
    """
    for script in soup(["script", "style"]):
        script.decompose()
    strips = list(soup.stripped_strings)
    return strips


def remove_stopwords(input_list):
    """
    :param input_list:
    :return: input_list without stop words
    """
    from nltk.corpus import stopwords

    stop_words = stopwords.words('english')  # to store all possible stop words
    no_stop_words = []  # to store words that are not not stop words
    for word in input_list:
        if word not in stop_words:
            no_stop_words.append(word)
    return no_stop_words


def get_text(content):
    """
    :param content:
    :return: string format of content
    """
    result_text = ""
    for con in content:
        if len(con.strip()) > 0:
            result_text = result_text + " " + con
    return result_text


def remove_punctuation(in_str):
    """
    :param in_str:input string
    :return: in_str with out punctuations
    """
    all_punctuation = string.punctuation  # to get all punctuation and storing it in punctuation
    table = in_str.maketrans('', '', all_punctuation)  # Making a table by passing only third argument only
    rem_str = in_str.translate(table)  # removing the punctuation from the in_str and storing it in rem_str
    return rem_str  # printing out the rem_str


def write_links(internal, external):
    """
    :param internal:
    :param external:
    writes the internal links in InternalLinks.txt file and
    external links in ExternalLinks.txt file
    """
    with open('InternalLinks.txt', mode='w') as content:
        for link in internal:
            content.write(link + "\n")
    with open('ExternalLinks.txt', mode='w') as content:
        for link in external:
            content.write(link + "\n")


def write_text(internal, url):
    """
    :param internal:
    :param url:
    writes all text from the webpage to TextContent
    """
    for link in internal:
        if url not in link:
            link = url + "/" + link
        soup_instance = get_soup(link)
        list_format = get_text_list_format(soup_instance)
        no_stop_words = remove_stopwords(list_format)
        text_format = get_text(no_stop_words)
        text = remove_punctuation(text_format)
        print(text)
        with open('TextContent.txt', mode='a', encoding='utf-32') as content:
            content.write(link + "\n")
            content.write(text + "\n")


def get_title(soup):
    """
    :param soup:
    :return: title of the soup element if exist
    """
    title = soup.select('title')
    if len(title) == 0:
        return "encoding decoding issues"
    else:
        return title[0].getText()


def write_page_title(internal, external, url):
    """
    :param internal:
    :param external:
    :param url:
    :return: writes the title of all links
    """
    with open('Title.txt', mode='a') as content:
        content.write("Internal Link Titles\n")
    for link in internal:
        if url in link:
            soup_instance = get_soup(link)
            title = get_title(soup_instance)
            with open('Title.txt', mode='a') as content:
                content.write(link + "\t" + title + "\n")
    with open('Title.txt', mode='a') as content:
        content.write("External Link Titles\n")

    for link in external:
        soup_instance = get_soup(link)
        title = get_title(soup_instance)
        with open('Title.txt', mode='a', encoding="utf-32") as content:
            content.write(link + "\t" + title + "\n")


def get_meta(soup):
    """
    :param soup:
    :return: meta data of the soup element if exist
    """
    meta = soup.select('meta')
    if len(meta) == 0:
        meta = ["encoding decoding issues"]
        return meta
    else:
        return meta


def write_meta_data(internal, external, url):
    """
    :param internal:
    :param external:
    :param url:
    :return:
    """
    with open('Metadata.txt', mode='a') as content:
        content.write("Internal Link meta data\n")
    for link in internal:
        if url in link:
            soup_instance = get_soup(link)
            meta_data = get_meta(soup_instance)
            with open('Metadata.txt', mode='a') as content:
                for data in meta_data:
                    content.write(link + "\t" + str(data) + "\n")

    with open('Metadata.txt', mode='a') as content:
        content.write("External Link Titles\n")

    for link in external:
        soup_instance = get_soup(link)
        meta_data = get_meta(soup_instance)
        with open('Metadata.txt', mode='a', encoding="utf-32") as content:
            for data in meta_data:
                content.write(link + "\t" + str(data) + "\n")


def write_main_page(text_content):
    with open('HomePageContent.txt', mode='a') as content:
        content.write(text_content)


def get_uni_gram():
    file = open('HomePageContent.txt')
    counts = {}
    for line in file:
        line = line.lower()
        words = line.split()
        for word in words:
            if word not in counts:
                counts[word] = 1
            else:
                counts[word] += 1
    order = list()
    for key, val in list(counts.items()):
        order.append((val, key))
    order.sort(reverse=True)
    return order


def write_uni_grams():
    file = open('top20_uni_gram.csv', mode="a", encoding='utf-8', newline='')
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['count', 'word'])
    uni_gram_values = get_uni_gram()
    for key, val in uni_gram_values[:20]:
        writer.writerow([key, val])
    file.close()
    file = open('uni_gram.csv', mode="a", encoding='utf-8', newline='')
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['count', 'word'])
    for key, val in uni_gram_values:
        writer.writerow([key, val])
    file.close()


def get_bi_grams():
    file = open('HomePageContent.txt')
    counts = {}
    content = file.readlines()[0].split(" ")
    for i in range(len(content)):
        word_1 = content[i - 1].strip()
        word_2 = content[i].strip()
        word = word_1 + " " + word_2
        word = word.lower()
        if word not in counts:
            counts[word] = 1
        else:
            counts[word] += 1
    order = list()
    for key, val in list(counts.items()):
        order.append((val, key))
    order.sort(reverse=True)
    return order


def write_bi_grams():
    file = open('top20_bi_gram.csv', mode="a", encoding='utf-8', newline='')
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['count', 'word'])
    uni_gram_values = get_bi_grams()
    for key, val in uni_gram_values[:20]:
        writer.writerow([key, val])
    file.close()
    file = open('bi_gram.csv', mode="a", encoding='utf-8', newline='')
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['count', 'word'])
    for key, val in uni_gram_values:
        writer.writerow([key, val])
    file.close()


def get_size(url):
    return url


'''
    import urllib.request
    site = urllib.request.urlopen(url)
    try:
        if type(site.length) == int:
        return float(site.length / 1000)
        else:
            return "Not Known"
    except:
        return "error"
'''


def write_site_size(internal, external, url):
    file = open('SiteSize.csv', mode="a", encoding='utf-8', newline='')
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['Site', 'Size(in kb)'])
    for link in internal:
        if url in link:
            size = get_size(link)
            writer.writerow([link, size])
    for link in external:
        size = get_size(link)
        writer.writerow([url, size])
    file.close()


home_url = get_home_url()
home_soup = get_soup(home_url)
internal_link, external_link = get_links(home_soup, home_url)
# write_links(internal_link, external_link)
# write_text(internal_link, home_url)
# write_page_title(internal_link, external_link, home_url)
# write_meta_data(internal_link, external_link, home_url)

text_list = get_text_list_format(home_soup)
no_stop_words_list = remove_stopwords(text_list)
text = get_text(no_stop_words_list)
no_punctuation_text = remove_punctuation(text)
# write_main_page(no_punctuation_text)
# write_uni_grams()
# write_bi_grams()
write_site_size(internal_link, external_link, home_url)
