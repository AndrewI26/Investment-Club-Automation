from leaders import getLeaders
from slides import updateSlides
from docs import updateDocs

def main():
    leaders = getLeaders()
    updateSlides(leaders)
    updateDocs(leaders)

if __name__ == "__main__":
    main()