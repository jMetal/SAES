References File
===============

The reference front data should be stored in a separate folder with the following structure:

.. code-block::

    📂 references_folder  
    ├── instance-1.ND.csv
    ├── instance-2.ND.csv          
    .
    .
    ├── instance-m.ND.csv          

Structure Details
-----------------

- Each **instance** has a corresponding reference front file.  
- The **"ND"** in the filename indicates the number of dimensions in the data.  
  - For example, if your data is **2D**, the files should be named as ``instance-1.2D.csv``, ``instance-2.2D.csv``, etc.  

By correctly setting up these data sources, you can ensure accurate Pareto front visualizations using the `Saes` multiobjective module.

