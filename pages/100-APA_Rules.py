PAGE_HEADER = 'Soaping'
PAGE_SUBHEADER = 'Cost Calculator'
SIDEBAR = 'collapsed'
MENU_ITEMS = {
       'SAP Calculator': '/SAP',
       'Cost Calculator': '/Cost'
}

from mods.base import *



st.markdown('''
            ### Margins never smaller than 1 inch on all sides

        ### Title/cover is first page. (ask instructor if required)

        #### Six components of title page (no abbreviations, centered, no text deco, normal case, centered, except as noted)

        -title (bold, title case)

        -all authors (no prefix, ),

        -institution,

        -course # and title,

        -instructor's name (use prefix they prefer),

        -due date

        ###body:

        1st line: page number upper right

        2nd line: title- bold, centered, title case

        next line: introduction paragraph, indented

        rest of body: first line of every paragraph indented

        headings: (double spaced, no extra lines)

        -L1: Title as above

        -L2: Left align, bold, case as needed

        -L3: L2 plus period at end.

        -L4: L3 plus indented

        -L5: L4 plus extra indent?

        ### Writing style:

        -Verbs, always use same tense throughout section

        -past or present perfect for explanation of procedures

        -past for explanation of results

        -present for explanation of conclusion and future implications

        ####Bias:

        #####Avoid bias towards:

        -Gender

        -Racial groups

        -Ages

        -Disabilities

        -Sexual orientation

        only include if needed for topic or study, 

        person first: “Diabetic patients” or “Patients who are diabetic”:

        use broad terms like “participants” or “subjects” instead of “elderly” or “gay”

        Firefighter instead of fireman or firewoman

        They/Their is acceptable

        Use census categories and capitalize first letter: Hispanic

        Don't use “minority”, connotates “less than” or “deficient”, use “People of Color” or “Under-represented group”

        Always use Oxford comma:  this, that, and the other   this, that, or the other

        ###Numbers:

        -< 10, written out in text, > 10 in numerals, except:

        -numbers in tables or graphs,

        -references to tables or graphs:  “Table 7” 

        -including unit of measure directly after: “8 lbs, 5 cm,  7 oz”

        -displaying math equations: "4 
        ''', unsafe_allow_html=True)


