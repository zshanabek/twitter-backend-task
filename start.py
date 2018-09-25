import twint

# Configure
c = twint.Config()
c.Username = "now"
c.Search = "pineapple"
c.Format = "Tweet id: {id} | Tweet: {tweet}"

# Run
twint.run.Search(c)