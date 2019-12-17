import pyperclip, itertools, pandas as pd

def format(JSON_input, heading_input):

    ### Read and format scraped field dictionary
    df = pd.read_csv("dictionary.csv", index_col=0)
    d = df.to_dict("split")

    data = list(itertools.chain(*d['data']))
    dictionary = dict(zip(data, d["index"]))
        
    ### Data formatting and setting up variables / dictionaries
    JSON   = JSON_input.split('{')[1].split('}')[0]
    fields = JSON.split('",')

    div         = ''
    properties  = []
    heading     = "<%%= %s %%>" % heading_input
    
    ### Creating the HTML string with headings, attributes and explanatory text
    for i in fields:
        prop = i.strip().split(":")[0].strip('"')
        properties.append(prop)

        if properties[0] == '_heading':
            properties.pop(0)

    for prop in properties:
        
        text = prop
        
        if prop in dictionary.keys():
            text = dictionary[prop]
        
        div = div + "<div> %s: <%%= %s %%> </div> " % (text, prop)
        
    html = "<div class='widget-hoverbox-title'> %s </div> <div class='widget-hoverbox-sub'> %s</div>" % (heading, div)
    
    return html
 

 
if __name__ == "__main__":

    ### Input JSON chunk and heading
    JSON_input = input("Paste JSON chunk here, starting from and including 'properties':")
    if not JSON_input.split('{')[1].split('}')[0].split(':')[0].strip().strip('"') == '_heading':
        heading_input = input("Define the heading attribute:")
    else:
        heading_input = '_heading'
    
    ### The output HTML is copied to clipboard
    html = format(JSON_input, heading_input)
    pyperclip.copy(html)
    
    print("\n\n\nThe formatted HTML code below (select and copy):\n")
    print(html)
    input("\n\nPress Enter to exit...")