![alt text](puddle.png)

### What it is
Puddle is a Python package and CLI that allows Machine Learning developers and enthusiasts to quickly and easily host their models, with a beautiful UI to showcase their models, with just one command

### How to use
1. Simply install the package using Pip,
2. Create a config.json file using `puddle gen-config proj-name` OR create a config.json manually
3. Deploy using `puddle deploy config.json`
4. Your unique webpage link will be displayed, usually oururl. com/models/proj-name

### Why this exists
There are too many models floating around online unused, that can be used by everyday people if the ML engineers had an easy way to share them. This takes care of the front-end, back-end component, and provides incredibly flexibility to engineers to be able to share their models easily. Think of it like the Github of Machine Learning Models. 

## TODO
1. Make model display page prettier
2. Make landing page for project
3. Create pipeline when user attempts to use model
   1. Accept Input,
   2. Validate input,
   3. Run input through run file,
   4. Get result,
   5. Display result
   
   

