#!/usr/bin/python3

import os
import json
import re
import argparse
import base64

# =========
# EXPLAINER
# =========

# Preparation for running
# - Create a directory where the input file will go
# - Place recipes in above directory in "Paprika Recipe Format" named 'MyRecipes.paprikarecipes'

# Data to include in each recipe
# - name
# - created
# - source
# - source_url
# - photo_data
# - categories
# - rating
# - description
# - ingredients
# - directions
# - notes
# - prep_time
# - cook_time
# - total_time
# - servings
# - nutritional_info


# =========
# ARGUMENTS
# =========
parser = argparse.ArgumentParser(description='Arguments for converting Paprika to MD.')

# this is the directory where the file to import is, as well as where temporary work will be done
parser.add_argument("-i","--indir", default='input', help="Directory to put the myRecipes.paprikarecipes file.")

# this is where the final files will be output
parser.add_argument("-o","--outdir", default='output', help="Output directory for markdown files.")


# =========
#  GLOBALS
# =========
args = parser.parse_args()
recipesName = 'myRecipes'
inputDir = args.indir+'/'
paprikaFile = inputDir + recipesName+'.paprikarecipes'
outputDir = args.outdir+'/'


# =========
#   START
# =========
print("PASSED ARGS: input = " + args.indir + "; output = " + args.outdir)


# ==========
# EXTRACTION
# ==========
# if the recipes aren't already exploded then do so
print("EXTRACTION: looking for " + paprikaFile)
if os.path.isfile(paprikaFile):
    print("  Recipe archive exists")
    # setup an array of the commands to run
    cmds = [
        # clean our blog _recipe directory
        'rm -rf ' + outputDir,
        # create our blog _recipe directory
        'mkdir -p ' + outputDir,
        # create img folder for output
        'mkdir -p ' + outputDir + '/img',
        # unzip the recipe archive
        'unzip -q '+paprikaFile+' -d ' + inputDir,
        # delete the recipe archive
        'rm '+paprikaFile,        
        # change file extension of each file to gz
        'for f in ' + inputDir + '*.paprikarecipe; do mv "$f" "${f%.paprikarecipe}.gz";done',
        # unzip individual recipe files
        'gzip -d '+ inputDir + '*.gz',
        # add file extension of json to each file
        'for f in ' + inputDir + '*; do mv -f "$f" "${f%}.json";done',
    ]
    # process each of our commands
    for cmd in cmds:
        print("  - Command: " + cmd)
        os.system(cmd)
else:
   print("  No recipe archive, attempting to convert individual recipes (if present)")


# ==========
# CONVERSION
# ==========
# grab all files in the input directory
inputFiles = os.listdir(inputDir)
# filter the list to only return json files - these are the ones we will convert
recipes = list(filter(lambda recipe: re.search(r'\.json$', recipe, re.I), inputFiles))

if len(recipes) == 0:
    print("CONVERSION: no individual recipes present. Quitting")
    quit()

# process each file in the recipe directory
print("CONVERTING " + str(len(recipes) - 1) + " recipe(s)")
for recipe in recipes:
    recipeFileIn = inputDir + recipe
    # create our output file name
    recipeFileOut = recipeFileIn
    recipeFileOut.replace('.json', '.md')
    
    # Open the recipe file & read the JSON
    recipeData = json.load(open(recipeFileIn))
    cleanName = re.sub('[\']', '', recipeData['name']).strip()
    recipePath = outputDir + cleanName+'.md'

    # NAME - frontmatter
    rNameFront = cleanName

    # CREATED DATE - frontmatter - yyyy-mm-dd
    rDate = '\ndate: ' + recipeData['created'][0:10]

    # SOURCE - frontmatter
    rSource = ''
    if recipeData['source'] and not recipeData['source'].isspace():
        rSource = '\nsource: '+recipeData['source']
    
    # NAME / SOURCE URL - markdown
    rNameHeading = cleanName
    if recipeData['source_url'] and not recipeData['source_url'].isspace():
        rNameHeading = '[' + cleanName + '](' + recipeData['source_url'] + ')'

    # PHOTO - markdown
    rPhoto = ''
    if recipeData['photo_data']:
        # encode the image, and set the filename to the recipe but URL friendly (eg "Apple Crumble.jpg => apple-crumble.jpg")
        imgData = base64.b64decode(recipeData['photo_data'])
        imgName = cleanName.lower().replace(' ','-')
        filename = outputDir + 'img/' + imgName + '.jpg'
        with open(filename, 'wb') as f:
            f.write(imgData)
        rPhoto = '\n\n![](img/' + imgName + '.jpg)'
    
    # CATEGORIES - markdown merge into a list of #tags #like #this
    rCategories = ''
    if recipeData['categories']:
        rCategories = '#' + ' #'.join(recipeData['categories'])

    # RATING - markdown
    rRating = ''
    if recipeData['rating']:
        rRating = '#' + str(recipeData['rating']) + "star"
    
    # TAGS - markdown 
    rTags = ''
    if rRating or rCategories:
        rTags = '\n> **tags**: ' + rCategories + ' ' + rRating

    # DESCRIPTION - markdown
    rDescription = ''
    if recipeData['description'] and not recipeData['description'].isspace():
        # remove all extra new lines, then space out paragraphs
        rDescription = re.sub('\n+', '\n', recipeData['description'])
        rDescription = '\n\n## Description\n' + re.sub('\n', '\n\n', rDescription)

    # INGREDIENTS - markdown list with subheadings
    rIngredients = '\n\n## Ingredients\n'
    for ingr in recipeData['ingredients'].split("\n"):
        if ingr.isspace():
            continue
        # replace fancy fractions with n/m
        ingr = re.sub('½','1/2', ingr)
        ingr = re.sub('⅓','1/3', ingr)
        ingr = re.sub('⅔','2/3', ingr)
        ingr = re.sub('¼','1/4', ingr)
        ingr = re.sub('¾','3/4', ingr)
        ingr = ingr.strip()
        
        # handle subheadings
        if ingr.endswith(':'):
           ingr = '\n### ' + ingr.replace(':','')
        # make ingredients a bulleted list
        elif ingr:
           ingr = "- " + ingr
        # only add non blank lines
        if ingr:
           rIngredients = rIngredients+ '\n' + ingr

    # DIRECTIONS - markdown
    rDirections = ''
    if recipeData['directions'] and not recipeData['directions'].isspace():
        # remove all extra new lines, then space out paragraphs
        rDirections = re.sub('\n+', '\n', recipeData['directions'])
        rDirections = '\n\n## Directions\n' + re.sub('\n', '\n\n', rDirections)

    # NOTES - markdown
    rNotes = ''
    if recipeData['notes'] and not recipeData['notes'].isspace():
        # remove all extra new lines, then space out paragraphs
        rNotes = re.sub('\n+', '\n', recipeData['notes'])
        rNotes = '\n\n## Notes\n' + re.sub('\n', '\n\n', rNotes)

    # GENERAL DATA = markdown
    rData= ''
    dataList = []
    if recipeData['prep_time']:
        dataList.append('**prep** ' + recipeData['prep_time'])
    if recipeData['cook_time']:
        dataList.append('**cook** ' + recipeData['cook_time'])
    if recipeData['total_time']:
        dataList.append('**total** ' + recipeData['total_time'])
    
    recipeData['servings']

    if len(rData) > 0 or recipeData['servings']:
        rData = '\n\n## Data\n'
    if len(rData) > 0:
        rData = rData + ' | '.join(dataList)
    if recipeData['servings']:
        rData = rData + ' | **serves** ' + recipeData['servings']

    # NUTRITION - markdown
    rNutrition = ''
    if recipeData['nutritional_info'] and not recipeData['nutritional_info'].isspace():
        # remove all extra new lines, then space out paragraphs
        rNutrition = re.sub('\n+', '\n', recipeData['nutritional_info'])
        rNutrition = '\n\n## Nutrition\n' + re.sub('\n', '\n\n', rNutrition)

    # FORMAT FINAL MARKDOWN STRING
    markdownTemplate = '---\ntitle: {nameFront}{date}{source}\n---\n# {nameHeading}{tags}{photo}{description}{ingredients}{directions}{notes}{data}'.format(
        nameFront=rNameFront,
        date=rDate,
        source=rSource,
        nameHeading=rNameHeading,
        tags=rTags,
        photo=rPhoto,
        description=rDescription,
        ingredients=rIngredients,
        directions=rDirections,
        notes=rNotes,
        data=rData,
    )

    # write out recipe markdown file
    file = open(recipePath, "w")
    file.write(markdownTemplate)
    file.close()
    print("  - Saved " + recipePath)

    # =======
    # CLEANUP
    # =======
    # currently disabled so to make it easier to edit the JSON files if needed then reimport by running the script again
    # print("CLEANUP: removing recipe file:" + recipeFileIn)
    # os.remove(recipeFileIn)