import unittest
from GIR import *

class GIR_Unit_Tests(unittest.TestCase):

    def setUp(self):
        example_file = '/global/cscratch1/sd/descpho/Pipeline-tasks/DC2-phoSim-3_WFD-r/000000/work/lsst_e_151687_f2_R43_S22_E000.fits.gz'
        
        self.example_instance = BaseImageReader(example_file)

    def tearDown(self):
        del self.example_instance

    def test_card_true(self):
        self.assertTrue(self.example_instance.has_card('date'))

    def test_card_false(self):
        self.assertFalse(self.example_instance.has_card('foo'))

    def test_cards_true(self):
        self.assertTrue(self.example_instance.has_cards(['creator','date']))

    def test_cards_false(self):
        self.assertFalse(self.example_instance.has_cards(['date','foo']))

    def test_size(self):
        self.assertEqual(self.example_instance.get_im_dim(), (4000,4072))
        

    
