import itertools
import numpy as np

from . import cfg

class NdIndexConverter(object):
    """Help for converting between 1d and Nd indices into arrays and
    iterating over them. This assumes that the arrays have a
    C-language ordering, i.e. last-fastest.
    """
    
    def __init__(self, shape):
        """shape is the number of elements along each dimension of the
        array.  """
        
        self.shape = np.array(shape).squeeze()
        self.ndim = len(self.shape)
        self._conv = np.array([np.prod(self.shape[i:]) for i in range(1, self.ndim+1)], dtype=np.int)
        return
    
    def OneToNd(self, one):
        """Go from a 1d index to an Nd index.
        """
        ans = np.zeros(self.ndim, dtype=np.int)
        for i in xrange(self.ndim):
            ans[i] = one / self._conv[i]
            one = one % self._conv[i]
            continue
        return ans

    def NdToOne(self, nd):
        """Go from an Nd index list to a 1d index.
        """
        return np.dot(nd, self._conv)

    def IterOne(self):
        """Return an iterator over the 1d indices.
        """
        return xrange(np.prod(self.shape))
    
    def IterNd(self):
        """Return an iterator over the Nd indices.
        """
        return itertools.imap(np.array, np.ndindex(tuple(self.shape)))

    def IterBoth(self):
        """Return an iterator yielding (1d, Nd) index tuples.
        """
        return itertools.izip(self.IterOne(), self.IterNd())
    
    pass

# ======================================================================
# Classes representing HemeLB objects
# ======================================================================

class Domain(object):
    """Spatial domain sampled by a HemeLB config file.

    Public attributes:

    - StressType
    - BlockCounts
    - BlockSize
    - VoxelSize
    - Origin
    - SiteCounts
    - TotalBlocks

    Public methods:

    - GetBlock(bIdx)
    - SetBlock(bIdx, block)
    - GetSite(sgIdx)
    
    """
    def __init__(self):
        self.StressType = None
        self._BlockCounts = None
        self._BlockSize = None
        
        self.VoxelSize = None
        self.Origin = None
        
        return
    
    @property
    def SiteCounts(self):
        return self.BlockCounts * self.BlockSize

    @property
    def BlockCounts(self):
        return self._BlockCounts
    
    @BlockCounts.setter
    def BlockCounts(self, bc):
        self._BlockCounts = bc
        self.Blocks = np.zeros(self.TotalBlocks, dtype=object)
        self.BlockIndexer = NdIndexConverter(bc)
        for ijk, i3 in self.BlockIndexer.IterBoth():
            self.Blocks[ijk] = NotYetLoadedBlock(self, i3)
            continue
        
        return
        
    @property
    def TotalBlocks(self):
        return np.prod(self._BlockCounts)

    @property
    def BlockSize(self):
        return self._BlockSize
    @BlockSize.setter
    def BlockSize(self, bs):
        self._BlockSize = bs
        self.BlockSiteIndexer = NdIndexConverter((bs,bs,bs))
        return
    
    def GetBlock(self, bIdx):
        if np.all(bIdx >= 0) and np.all(bIdx < self.BlockCounts):
            return self.Blocks[self.BlockIndexer.NdToOne(bIdx)]
        else:
            return OutOfDomainBlock(self, bIdx)
        
    def SetBlock(self, bIdx, block):
        if np.all(bIdx >= 0) and np.all(bIdx < self.BlockCounts):
            self.Blocks[self.BlockIndexer.NdToOne(bIdx)] = block
        else:
            raise ValueError('Block index out of range')

    def DeleteBlock(self, bIdx):
        """Ensure that the circular references from Sites to their
        containing Block are deleted.
        """
        self.GetBlock(bIdx).DeleteSites()
        self.SetBlock(bIdx, None)

    def GetSite(self, sIdx):
        bIdx = sIdx / self.BlockSize
        block = self.GetBlock(bIdx)
        return block.GetLocalSite(sIdx % self.BlockSize)

    pass

class Block(object):
    """A macro-block, typically 8x8x8, but this is variable here.

    Public attributes:

     - Domain
     - Index

    Public methods:

     - GetSite(sgIdx)
    """
    def __init__(self, domain, index):
        self.Domain = domain
        self.Index = index
        self.nFluidSites = 0
        self.Sites = None
        return

    def GetLocalSite(self, slIdx):
        assert np.all(slIdx >= 0) and np.all(slIdx < self.Domain.BlockSize)
        return self.Sites[self.Domain.BlockSiteIndexer.NdToOne(slIdx)]

    def GetSite(self, sgIdx):
        return self.Domain.GetSite(sgIdx)

    def DeleteSites(self):
        del self.Sites
        return
    
    pass

    
class NotYetLoadedBlock(Block):
    def GetLocalSite(self, sIdx):
        raise ValueError('Cannot get sites from NotYetLoadedBlock')
    pass


class Site(object):
    def __init__(self, block, sgIdx):
        self.Block = block
        self.Index = sgIdx
        
        self.Config = None
        self.Position = block.Domain.Origin + block.Domain.VoxelSize * sgIdx
        
        self.BoundaryNormal = None
        self.BoundaryDistance = None
        self.WallNormal = None
        self.WallDistance = None

        self.CutDistances = None
        
        return
    
    @property
    def Type(self):
        return cfg.GetType(self.Config)
    @property
    def BoundaryConfig(self):
        return cfg.GetType(self.Config)
    @property
    def BoundaryId(self):
        return cfg.GetBoundaryId(self.Config)
    @property
    def Edge(self):
        return bool(cfg.GetPressureEdge(self.Config))
    
    pass

class OutOfDomainBlock(Block):
    
    def GetLocalSite(self, slIdx):
        assert np.all(slIdx >= 0) and np.all(slIdx < self.Domain.BlockSize)
        return OutOfDomainSite(self)
    
    pass

class OutOfDomainSite(Site):
    def __init__(self, block):
        self.Config = cfg.SOLID_TYPE
        self.Block = block
        return
    pass


class AllSolidBlock(Block):

    def GetLocalSite(self, slIndx):
        assert np.all(slIndx >= 0) and np.all(slIndx < self.Domain.BlockSize)
        return AllSolidSite(self, slIndx)

    pass

class AllSolidSite(Site):
    def __init__(self, block, sgIdx):
        self.Block = block
        self.Index = sgIdx
        self.Config = cfg.SOLID_TYPE
        return
    pass
