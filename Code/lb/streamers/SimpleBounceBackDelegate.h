// 
// Copyright (C) University College London, 2007-2012, all rights reserved.
// 
// This file is part of HemeLB and is CONFIDENTIAL. You may not work 
// with, install, use, duplicate, modify, redistribute or share this
// file, or any part thereof, other than as allowed by any agreement
// specifically made by you with University College London.
// 

#ifndef HEMELB_LB_STREAMERS_SIMPLEBOUNCEBACKDELEGATE_H
#define HEMELB_LB_STREAMERS_SIMPLEBOUNCEBACKDELEGATE_H

#include "lb/streamers/BaseStreamerDelegate.h"
#include "lb/streamers/SimpleCollideAndStream.h"

namespace hemelb
{
  namespace lb
  {
    namespace streamers
    {

      template<typename CollisionImpl>
      class SimpleBounceBackDelegate : public BaseStreamerDelegate<CollisionImpl>
      {
        public:
          typedef CollisionImpl CollisionType;
          typedef typename CollisionType::CKernel::LatticeType LatticeType;

          static inline site_t GetBBIndex(site_t siteIndex, int direction)
          {
            return (siteIndex * LatticeType::NUMVECTORS) + LatticeType::INVERSEDIRECTIONS[direction];
          }

          SimpleBounceBackDelegate(CollisionType& delegatorCollider, kernels::InitParams& initParams)
          {
          }

          inline void StreamLink(const LbmParameters* lbmParams,
                                 geometry::LatticeData* const latticeData,
                                 const geometry::Site<geometry::LatticeData>& site,
                                 kernels::HydroVars<typename CollisionType::CKernel>& hydroVars,
                                 const Direction& direction)
          {
            // Propagate the outgoing post-collisional f into the opposite direction.
            * (latticeData->GetFNew(GetBBIndex(site.GetIndex(), direction))) = hydroVars.GetFPostCollision()[direction];
          }

      };

    }
  }
}

#endif /* HEMELB_LB_STREAMERS_SIMPLEBOUNCEBACKDELEGATE_H */
