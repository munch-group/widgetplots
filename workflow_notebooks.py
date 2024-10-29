# %% [markdown]
# ---
# title: GWF workflow for notebooks
# execute:
#   eval: false
# ---

# %%
from pathlib import Path
from gwf import Workflow, AnonymousTarget
from gwf.workflow import collect

# %% [markdown]
"""
Instantiate the workflow with the name of the project folder.
"""

# %%
# instantiate the workflow
gwf = Workflow(defaults={'account': 'your-project-folder-name'})


# %% [markdown]
"""
## Template functions:
"""
# %%

# task template function
def run_notebook(path, memory='8g', walltime='00:10:00', cores=1):    
    """
    Executes a notebook inplace and saves the output.
    """
    # path of output sentinel file
    sentinel = path.parent / '.' + path.name

    # input specification
    inputs = [path]
    # output specification mapping a label to each file
    outputs = {'sentinel': sentinel}
    # resource specification
    options = {'memory': memory, 'walltime': walltime, 'cores': cores} 

    # commands to run in task (bash script)
    spec = f"""
    jupyter nbconvert --to notebook --execute --inplace path
    """
    # return target
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)

# %% [markdown]
"""
## Workflow:

Executes all notebooks in the `notebooks` directory in sorted order.
"""

# %%


dependencies = []
# run notebooks in sorted order nb01_, nb02_, ...
for notebook in Path('notebooks/**.ipynb'):
    # run a notebook
    target = run_notebook(notebook, dependencies)
    # make each notebook dependent on all previous
    dependencies.append(target.outputs['sentinel'])
    # add target to workflow
    gwf.target(target)


