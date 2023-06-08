import nibabel.tmpdirs as nbtmp
import nibabel as nib

import os.path as op
import numpy.testing as npt

import dipy.core.gradients as dpg
from dipy.data import default_sphere
from dipy.reconst.gqi import GeneralizedQSamplingModel

from AFQ.utils.testing import make_dki_data
from AFQ._fixes import gwi_odf


def test_GQI_fix():
    with nbtmp.InTemporaryDirectory() as tmpdir:
        fbval = op.join(tmpdir, 'dki.bval')
        fbvec = op.join(tmpdir, 'dki.bvec')
        fdata = op.join(tmpdir, 'dki.nii.gz')
        make_dki_data(fbval, fbvec, fdata)
        gtab = dpg.gradient_table(fbval, fbvec)
        data = nib.load(fdata).get_fdata()

        gqmodel = GeneralizedQSamplingModel(
            gtab,
            sampling_length=1.2)

        odf_ours = gwi_odf(gqmodel, data)

        odf_theirs = gqmodel.fit(data).odf(default_sphere)

        npt.assert_array_almost_equal(odf_ours, odf_theirs)
