
from __future__ import print_function

import numpy as np
import netCDF4
import re
from .base_grid import BaseGrid

class UMGrid(BaseGrid):

    def __init__(self, grid, mask_file=None):
        self.type = 'Arakawa C'
        self.full_name = f'UM {grid}'
        description = f"UM ENDGAME {grid}"

        reg = re.compile('n(\d+)e_([tuv])')
        m = reg.search(grid)
        if not m:
            raise Exception('Error parsing UM grid string')

        nlon_t = 2 * int(m.group(1))
        grid = m.group(2).lower()

        assert nlon_t % 4 == 0
        nlat_t = 3 * nlon_t // 4
        dx = 360.0 / nlon_t
        dy = 180.0 / nlat_t
        dx_half = dx / 2.
        dy_half = dy / 2.

        # Set lats and lons.
        lon_t = dx_half + np.linspace(0, 360, nlon_t, endpoint=False)
        lat_t = dy_half + np.linspace(-90, 90, nlat_t, endpoint=False)

        lat_u = lat_t
        lon_u = np.linspace(0, 360, nlon_t, endpoint=False)

        lon_v = lon_t
        nlat_v = nlat_t + 1
        lat_v = np.linspace(-90, 90, nlat_v)

        if mask_file is not None:
            with netCDF4.Dataset(mask_file) as f:
                # Expect mask file to have 0 for ocean, 1 for masked out land
                mask = f[f'mask_{grid}'][:]
        else:
            mask = None

        if grid == 't':
            lon, lat = lon_t, lat_t
        elif grid == 'u':
            lon, lat = lon_u, lat_u
        elif grid == 'v':
            lon, lat = lon_v, lat_v
        else:
            raise Exception(f"Incorrect grid {grid} specified in UMGrid")

        super(UMGrid, self).__init__(x_t=lon, y_t=lat, mask_t=mask,
                                     description=description)
