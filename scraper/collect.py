from bs4 import BeautifulSoup
from scraper.jls_project import scrape_jobs

def collect_data(required_role, required_location):
    scraped_linkedin, scraped_indeed, scraped_glassdoor = scrape_jobs(required_role, required_location)
    job_listings = []

    for linkedin_html in scraped_linkedin:
        try:
            soup = BeautifulSoup(linkedin_html, "html.parser")

            company = soup.find("div", class_="artdeco-entity-lockup__subtitle")
            company = company.get_text(strip=True) #if company else "Unknown"

            role = soup.find("a", class_="job-card-container__link").find("strong")
            role = role.get_text(strip=True) #if role else "Unknown"

            location = soup.find("div", class_="artdeco-entity-lockup__caption")
            location = location.find("span").get_text(strip=True) if location else "Unknown"

            link = soup.find("a", class_="job-card-container__link")
            link = "https://www.linkedin.com" + link["href"] #if link else "#"

            if required_location.lower() == "bangalore":
                required_location = "bengaluru"

            if required_location.lower() in location.lower():
                job_listings.append({
                    "company": company,
                    "role": role,
                    "location": location,
                    "link": link
                })
        except Exception as e:
            pass
    
    for indeed_html in scraped_indeed:
        try:
            soup = BeautifulSoup(indeed_html, "html.parser")

            c = soup.find("span", attrs={"data-testid": "company-name"})
            company = c.get_text()

            # Extract job role
            r = soup.find("h2", attrs={"class": "jobTitle"})
            role = r.get_text()

            # Extract location
            loc = soup.find("div", attrs={"data-testid": "text-location"})
            location = loc.get_text()

            # Extract job link
            l = soup.find("a", attrs={"class": "jcs-JobTitle"})
            link = "https://in.indeed.com" + l["href"]

            job_listings.append({
                    "company": company,
                    "role": role,
                    "location": location,
                    "link": link
                })
            
        except Exception as e:
            pass
        
        
    for glassdoor_html in scraped_glassdoor:
        try:
            soup = BeautifulSoup(glassdoor_html, "html.parser")

            # Extract company name
            c = soup.find("span", class_="EmployerProfile_compactEmployerName__9MGcV")
            company = c.get_text(strip=True)

            # Extract job role
            r = soup.find("a", class_="JobCard_jobTitle__GLyJ1")
            role = r.get_text(strip=True)

            # Extract location
            loc = soup.find("div", class_="JobCard_location__Ds1fM")
            location = loc.get_text(strip=True)

            # Extract job link
            l = soup.find("a", class_="JobCard_jobTitle__GLyJ1")
            link = l["href"]

            if required_location.lower() in location.lower():
                job_listings.append({
                        "company": company,
                        "role": role,
                        "location": location,
                        "link": link
                    })
            
        except Exception as e:
            pass

    return job_listings
