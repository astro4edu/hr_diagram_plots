## What this repository does	
This plot makes a Hertzsprung-Russell diagram that shows the main luminosity classes as well as radius and colour for each object.

## Where does the data come from?
Most data from this plot comes from the [ESA Gaia mission](https://sci.esa.int/web/gaia). The majority of stars plotted here come from three samples:

- One selecting Gaia stars within 8pc
- One selecting 2.5% of the Gaia stars with parallax<10(G-5). Where ESA Gaia does not quote a luminosity, we use a luminosity calculated from the estimated radius and temperature of the star.
- A subsample of stars from the [Pickles (1998)](https://ui.adsabs.harvard.edu/abs/1998PASP..110..863P/abstract) spectral library. This was added to include a wider range of spectra types
- White dwarfs within 12pc from [Vincent et al. (2024)](https://ui.adsabs.harvard.edu/abs/2024A%26A...682A...5V/abstract). 
- A selection of named stars selected by hand to add named stars across the different temperatures and luminosity classes
For named stars the luminosity, temperature and radius estimates are taken from the literature. See the named stars table in the data folder for references.  Our
These samples were chosen to provide objects across the HR diagram and do not provide a representative sample of stars in the Galaxy.

In the first three samples the selected stars had parallaxes ten times greater than their parallax uncertainties, had Gaia G magnitudes brighter than 18, were not flagged as non-single stars and had Renormalised Unit Weight Error (RUWE) less than 1.4 as recommended by [Lindegren et al. (2018)](https://www.cosmos.esa.int/documents/29201/1770596/Lindegren_GaiaDR2_Astrometry_extended.pdf/1ebddb25-f010-6437-cb14-0e360e2d9f09). 

In the first three samples the selected stars we used data from the Gaia DR3 astrophysical parameters table. We used effective temperatures and radius estimates in this table derived from Gaia photometry and where available the luminosity from the FLAME pipeline. Where this was not available we estimated the luminosity from the effective temperature and radius estimates. For the white dwarfs we used the parameters from Vincent et al. (2024). For the named stars we used luminosities, radii and temperatures from a range of source (see the data table for named stars for more details).

The colours for our objects are generated using the relationships in [Harre & Heller (2021)](https://onlinelibrary.wiley.com/doi/10.1002/asna.202113868). For most objects we use the T_eff + log g grid (table 2 in Harre & Heller), for stars hotter than 10,000K we use the temperature/spectral type relationship (table 5) and white dwarfs we use the effective temperature relationship for blackbodies (table 1).
## How to create plots using this repository
The command to run code from this repository is:
`python3 hr_diagram_plot.py`
The following command line options are available:
```-h, --help            show this help message and exit
  --lang LANG           add language code
  --plot_dir PLOT_DIR   add directory for output plots. Default is plots directory in this repository.
  --translations_file TRANSLATIONS_FILE
                        add your own JSON file containing translations. Default is translations.json in this repository.
  --output_format OUTPUT_FORMAT
                        add the output format for the plots. options: eps, jpg, jpeg, pdf, pgf, png, ps, raw, rgba,
                        svg, svgz, tif, tiff. Default is png.
  --translate_filenames TRANSLATE_FILENAMES
                        If True output filenames will be in requested language. If False output filenames will be in
                        English. Default is False
```
Example usage, for English, using untranslated filenames, the default translation file, pdf output format and output directory "/home/user/plots/", one would use the command:
```python3 hr_diagram_plot.py --lang=en --output_format=pdf --plot_dir=/home/user/plots/ ```
The code creates an example plot.

## License
The code released is available under an MIT license and should be credited to IAU OAE/Niall Deacon. The plots in the plots directory and the translations in the translations directory are published under a <a href="https://creativecommons.org/licenses/by/4.0/deed.en">CC-BY-4.0 license</a>. For the data included in the data folder please cite the source paper and/or Gaia. 

## Plot Credits
Please credit all plots created by this code to IAU OAE/Niall Deacon. For languages other than English, please also credit the translators listed below. 
<!-- start-translation-credits -->

## Translation credits

<!-- end-translation-credits -->

## Adding your own translation
You can add your own translations by downloading this repository and editing the translations.json file. Each language starts with a [language code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) followed by translations of each text element. We have included a placeholder `zz` language code that you can edit (or copy and edit if you want to add more than one language). For example if you were to translate the terms into German you would edit:
```
 "zz": {
    "translation_approval_level": "N",
    "translation_credit": null,
    "matplotlib_cairo": false,
    "possible_fonts": [
      "Noto Sans",
      "Arial"
    ],
    "title_text": "A title",
    "xaxis_text": "Some text",
    "yaxis_text": "Some more text",
  },
```
And instead have:
```
  "de": {
    "translation_approval_level": "N",
    "translation_credit": null,
    "matplotlib_cairo": false,
    "possible_fonts": [
      "Noto Sans",
      "Arial"
    ],
    "title_text": "ein Titel",
    "xaxis_text": "etwas Text",
    "yaxis_text": "noch etwas Text",
  },
```

Then just run:
```python3 hr_diagram_plot.py --lang=zz```
With `zz` replaced by your language code.

<!-- start-diagram-links -->

## Diagram Links
 Below are links to the diagrams produced by this code. You can also find the diagram captions and any translations of these captions in the links.
 <ul>
</ul>

<!-- end-diagram-links -->


## Fonts
The built-in fonts for matplotlib often struggle with non-Latin characters. The code is set up to try to load commonly used fonts for the writing system it is producing the plots for. If you want to load a font that is already installed on your system then you can tell the code to use that font by adding it to the start of the list in the `possible_fonts` list in `translations.json`. If you are struggling to get a particular writing system to work with this code then you can download the font you want to use and copy the `.ttf` file to the `fonts` folder of this repository. The code will then automatically load that font. The Google <a href="https://fonts.google.com/noto">Noto Fonts</a> project provides fonts in a wide range of writing systems. For some writing systems (mostly scripts used in South Asia such as Devanagari or Bengali) we recommend you use the <a href="https://pypi.org/project/mplcairo/">mplcairo matplotlib backend</a>. Once you have installed mplcairo, change "matplotlib_cairo" from false to true (lowercase, no quotemarks). We do not include mplcairo in the requirements.txt file as it is a little complex to install and only required by some users.

## Important Caveats

For languages other than English, please check the translation approval level in the translations.json file. If approval level is marked as 'N' then the translation has not been reviewed, translations marked 'Y' have been approved by a reviewer in our review system.
