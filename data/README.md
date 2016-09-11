#Structure of this folder
* bhajans.json - the main data file containing all the bhajans.
    * ```
      Structure of file:
        Json Dict {
            next_id : <int>,
            bhajans : list of Json Dict [
                    Json Dict { id: int
                                name: string
                                bhajan: string
                                meaning: string (optional)
                            }
                    ]
                  }```
* filler.jpg - The image used for backgrounds on filler slides.
* title_slide.jpg - The image used for the title slide.
* backgrounds/ - a folder containing images used as backgrounds(chosen at random) for bhajans
    * These images are best when a Gradient is applied to them(preferably dark colors like dark grey)
    * http://www194.lunapic.com/editor/?action=blend - a site to add gradient to images.