# Paprika to Markdown
Converts a paprika recipe export file to markdown files with images

## Summary
Export all your recipes from the Paprika 3 app and converts them all to standard markdown files, with images. It uses Python3 and has been started on Mac OS only.

**Quick steps**

1. clone this repo locally (or download it using the download link)
2. delete the example .json and .md file in the input and output folder
3. export your recipes in the Paprika format from Paprika 3
4. rename that file to "myRecipes.paprikarecipes"
5. place that file in the "input" folder of this repo
6. open a terminal window to the root folder of the repo
7. enter the command `./paprikaToMd.py` - this is the only code in the whole repo, the rest is there to help out

## Background
This is a fork of [this repo](https://gitlab.com/briankohles/paprika-to-grocery-markdown) - **thanks so much to Brian Kohles** for doing most of the heavy lifting!! That project aimed to convert Paprike recipes to the [Grocery App Markdown Format](https://github.com/cnstoll/Grocery-Recipe-Format), but this repo keeps things simpler (and fixes a number of bugs).

I like Paprika and have used it for years, but I wanted something:

- more cross-platform
- simpler - because I only really use the recipe part of Paprika and my recipes are pretty simple
- easier to edit and share
- that had less tie in to a proprietary app
- that I could edit in a more flexible way (like maybe eventually how the Grocery app does things)

Markdown is the obvious choice. I discovered the above repo and was very excited, but quickly ran into problems (both some bugs and a difference in preferences). I updated the code for the following use case:

- each recipe is a single markdown file using standard markdown
- each recipe has limited front matter for use in tools that support it, but nothing essential is in there 
- each recipe can have tags for apps that support that (as many do)
- all recipes will live in a single folder for use anywhere (eg in any markdown app or something like [Obsidian](https://obsidian.md))
- all images live in a single img folder

## How to export recpies from Paprika 3
1. In **Paprika Recipe Manager 3** choose `File` and `Export...`
2. From the Export dialog that opens choose the following options:

   1. **Save As** - Name the export file as `myRecipes.paprikarecipes` (use this exact case)
   2. Choose the directory location for the `import` directory of this project folder.
   3. **Categories** - `All Recipes`
   4. **Format** - `Paprika Recipe Format` - this is a single zipped file of all your recipes together 
   5. **Use Unicode Filenames** - `Yes`
   6. Click `Export` to create the file

## Running the script
The script lives in the **paprikaToMd.py** file. This script does the following things:

- looks in the `input` folder for a `myRecipes.paprikerecipes` file. This is just a zip file, so we unzip it to extract all the individual recipe files. These are each a gzipped json file, so we unzip each to leave us with a folder full of recipes in json files
- next we look for any json files (if the `myRecipes.paprikerecipes` file doesn't exist we also do this - this makes it easier to run the script again if you need to edit any of the json files instead of starting from scratch again)
- for each json file, we convert the json data into a nice looking markdown document. This md file is saved to the `output` folder. If a recipe has an image (which is embedded as a base64 encoded string in the json) we save the image in a url friendly name in the `output\img` folder. 

I have been a little opinionated in the exact format I have used for the markdown, so please feel free to fork this to make it work how you like. Or rework the markdown files after by using regex (which could, for instance, put all the tags into the frontmatter).

I also recommend that you review your recipes after to tidy them up or make sure they look ok.

**NOTE** the original author added command line arguments to the script. They are correctly setup but are not needed for basic use. I also have not tested them, but they will let you specify different input and output folders (e.g. `./paprikaToMd.py -i input -o output`)

**The script requires python3.**

## Known limitations
For some reason the paprika recipe files do NOT store "favorite" information. So you will have to add this manually afterwards
