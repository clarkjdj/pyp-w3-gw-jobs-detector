import click
import requests
from collections import Counter, defaultdict
from bs4 import BeautifulSoup
try:
    from jobs_detector import settings
except:
    import settings


#DEFAULT_KEYWORDS =  DEFAULT_KEYWORDS = [
DEFAULT_KEYWORDS = [
    'Remote',
    'Postgres',
    'Python',
    'Javascript',
    'React',
    'Pandas'
  ]


#@click.group()
#def jobs_detector():
#    pass


#@jobs_detector.command()
@click.command()
@click.argument('site')
@click.option('-i', '--post-id', type=str, required=True)
@click.option('-k', '--keywords', type=str, default=','.join(DEFAULT_KEYWORDS))
@click.option('-c', '--combinations', type=str,
              callback=lambda _, x: x.split(',') if x else x)
def jobs_detector(site, post_id, keywords, combinations):
    """
    This subcommand aims to get jobs statistics by parsing "who is hiring?"
    HackerNews posts based on given set of keywords.
    """
    # HINT: You will probably want to use the `BeautifulSoup` tool to
    # parse the HTML content of the website
    # page = requests.get(settings.BASE_URL.format(post_id))
    # soup = BeautifulSoup(page.text, 'html.parser')
    # 
   
    keywords = keywords.split(',')
    keywords = [keyword.title() for keyword in keywords] # make sure uppercase
     
    combinations = combinations or [] 
    combinations = [combo.title() for combo in combinations]
    #click.echo(combinations) 
    keyword_counts = defaultdict(int) 
     
    # get html
    html_doc  = requests.get(settings.BASE_URL.format(post_id))    #get post_id to requests object
    #make soup
    #soup = BeautifulSoup(html_doc.text, 'html.parser') #I'm not sure what response.text does, but I guess it strips HTML tags, we should be using response.content instead
    soup = BeautifulSoup(html_doc.content, 'html.parser')

    #posts = soup.find_all("tr", class_='athing') #Remoed because class=c00 is a better marker for the job posts
    posts = soup.find_all(class_="c00")
    job_posts = [job.get_text().lower() for job in posts]
    #job_posts = [post for post in posts if post.find_all("img", width="0")] #Removed becase class = c00 is a bettermarker for the job posts
    
    for post in job_posts:
        for key in keywords:
            if key.lower() in post:
                keyword_counts[key] +=1
        
        for combination in combinations: # for each possible combination
            combo_keywords = combination.lower().split('-') #divide into words in the combo
            #for post in job_posts: #then for each post #I don't think looping again through the posts makes much sense
                #if combo_keywords in set(post): #if all combo words in that post, +1. #I don't think this line makes much sense
            if all([keyword.lower() in post for keyword in combo_keywords]):
                keyword_counts[combination] += 1 
        
    total_num_posts = len(job_posts)

    #Results print out
    click.echo('Total job posts: {}\n'.format(total_num_posts))
    
    display_info('Keywords', keyword_counts, keywords, total_num_posts)
    
    if combinations:
        display_info('Combinations', keyword_counts, combinations, total_num_posts)
        

def display_info(name, keyword_counts, key_list, total_num_posts):

     click.echo('{}:'.format(name))
     for key in key_list:
         count = keyword_counts[key]
         try:
             percent = int(count / float(total_num_posts) * 100)
         except ZeroDivisionError:
             percent = 0
         click.echo('{}: {} ({}%)'.format(key, count, percent))



if __name__ == '__main__':
    jobs_detector()
