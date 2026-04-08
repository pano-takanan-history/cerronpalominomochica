import pathlib
from collections import defaultdict
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import FormSpec
from lingpy import Wordlist


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "cerronpalominomochica"
    form_spec = FormSpec(separators=";,~/", replacements=[(" ", "_")])

    writer_options = {'keep_languages': False, 'keep_parameters': False}

    def cmd_download(self, _):
        ...

    def cmd_makecldf(self, args):
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        concepts = {}
        for concept in self.concepts:
            args.writer.add_concept(
                    ID=concept["ID"],
                    Name=concept["GLOSS"]
                    #Concepticon_ID=concept["Concepticon_ID"],
                    #Concepticon_Gloss=concept["Concepticon_Gloss"]
                    )
            concepts[concept["GLOSS"]] = concept["ID"]
        args.log.info("added concepts")

        # add languages
        languages = {}
        for language in self.languages:
            args.writer.add_language(
                    ID=language["ID"],
                    Name=language["Name"],
                    Glottocode=language["Glottocode"]
                    )
            languages[language["Name"]] = language["ID"]

        args.log.info("added languages")

        wl = Wordlist(str(self.raw_dir.joinpath("raw.tsv")))

        # add data
        for (
            _,
            number,
            value,
            concept,
            doculect
        ) in pb(
            wl.iter_rows(
                "set",
                "form",
                "concept",
                "doculect"
            ),
            desc="cldfify"
        ):
            if value:
                args.writer.add_forms_from_value(
                    Language_ID=languages[doculect],
                    Parameter_ID=concepts[concept],
                    Value=value,
                    Source="Cerron"
                    )
