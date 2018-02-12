from astropy.io import fits, ascii
import numpy as np
import warnings

class BaseImageReader(object):
    """
    Abstract base class for image access.
    """


    def __init__(self,filename,**kwargs):
        self._init_kwargs = kwargs.copy()
        hdu_list = fits.open(filename)
        #for now i assume the images are supposed to have 1 fits extension
        #this is the case for the images i've looked at
        num_hdu = len(hdu_list)
        if num_hdu > 1:
            raise ValueError("file has: {0} extensions, only 1 fits extension files are allowed".format(num_hdu))

        #first we add meta data attributes 

        #this is an astropy header, which I'm anticipating is more than
        #users may want. But we will provide it and also give useful shortcuts
        self.header_astropy = hdu_list[0].header
        self.cards = list(self.header_astropy.keys())
        header_vals = [self.header_astropy[c] for c in self.cards]
        self.header_dict = dict(zip(self.cards,header_vals))

        #second add attributes dealing with the image data

        #is it memory efficent to keep image data as an attribute?
        self.im_data = hdu_list[0].data
        self.dimensions = self.im_data.shape[::-1]
        self.width = self.dimensions[1]
        self.height = self.dimensions[0]


    def get_header_as_astropy(self):
        """
        Returns
        -------
        header_as_astropy: astropy header
           fits header as returned by astropy
        """
        return self.header_astropy

    def get_header_as_dict(self):
        """
        Returns
        -------
        header_dict: dict
           dictionary containing header cards and values 
        """
        return self.header_dict

    def get_im_data(self):
        """
        Returns
        -------
        im_data: np.array
           the fits data associated with this image
        """
        return self.im_data

    def get_im_dim(self):
        """
        Returns
        -------
        dimensions: tupple
           width and height in pixels of the image
        """
        return self.dimensions

    def get_height(self):
        """
        Returns
        -------
        height: int
           how many pixels high the image is
        """
        return self.height

    def get_width(self):
        """
        Returns
        -------
        width: int
           how many pixels wide the image is
        """
        return self.width

    def list_all_cards(self, ):
        """
        return a python list of all the header cards
        """
        return self.cards

    def has_card(self, card):
        """
        Check if *card* is in the header

        Parameters
        ----------
        card: str
           the fits header keyword you want to check

        Returns
        -------
        has_card: bool
           True if the card is in the header; otherwise False 
        """
        #capitalize the header card for ease for the user
        return card.upper() in self.cards

    def has_cards(self, cards):
        """
        Check if ALL *cards* are header keywords available

        Parameters
        ----------
        cards: iterable
           list of card names to check. items should be strings

        Returns
        -------
        has_cards : bool
           True if all cards are available headery keywords; otherwise False
        """
        cards = set(cards)
        #capitalize the header cards for ease for the user
        return all(c.upper() in self.cards for c in cards)
