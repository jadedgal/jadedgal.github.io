from bs4 import BeautifulSoup, Comment
import re

title = input("Enter the title of the review: ")
review = input("Enter the review: ")

with open("index.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

accordion = soup.find("div", class_="accordion")
if accordion is None:
    raise ValueError("No accordion container found in HTML.")

existingItems = accordion.find_all("div", class_="accordion-item")

# Find all existing heading IDs and extract numbers
existingIndices = []
for item in existingItems:
    header = item.find("h2", class_="accordion-header")
    if header and header.has_attr("id"):
        # IDs like 'heading0', 'heading1' etc.
        match = re.search(r'(\d+)', header['id'])
        if match:
            existingIndices.append(int(match.group(1)))

# Determine next index
i = max(existingIndices) + 1 if existingIndices else 0
newItem = soup.new_tag("div", **{"class": "accordion-item"})
newItem.append(BeautifulSoup(f'''
    
    <h2 class="accordion-header" id="heading{i}">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
            data-bs-target="#collapse{i}" aria-expanded="false" aria-controls="collapse{i}">
            {title}
        </button>
    </h2>
    <div id="collapse{i}" class="accordion-collapse collapse" aria-labelledby="heading{i}"
        data-bs-parent="#accordionExample">
        <div class="accordion-body">
            {review}
        </div>
    </div>
''', "html.parser"))
accordion.append(newItem)
with open("index.html", "w", encoding="utf-8") as file:
    file.write(str(soup.prettify()))

print("Accordion item inserted with ID", i, "and file updated.")

