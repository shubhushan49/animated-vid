let a_tags = document.getElementsByClassName("gr-hyperlink")
let filtered_a_tags = Array.from(a_tags).filter(a => a.classList.length === 1)

let urls = filtered_a_tags.map(tag => tag.href)
let quotes = filtered_a_tags.map(tag => tag.innerText.split("Quotes")[0].trim())

let quotes_to_urls = {}

for (let i = 0; i < urls.length; i++) {
    quote_key = quotes[i]
    if (!quote_key) {
        quote_key = "Default"
    }
    quotes_to_urls[quote_key] = urls[i]
}