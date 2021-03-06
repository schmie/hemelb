//
// Copyright (C) University College London, 2007-2012, all rights reserved.
//
// This file is part of HemeLB and is CONFIDENTIAL. You may not work
// with, install, use, duplicate, modify, redistribute or share this
// file, or any part thereof, other than as allowed by any agreement
// specifically made by you with University College London.
//

#ifndef HEMELB_NET_MPIGROUP_H
#define HEMELB_NET_MPIGROUP_H

#include "units.h"
#include "net/mpi.h"
#include "net/MpiCommunicator.h"
#include <boost/shared_ptr.hpp>

namespace hemelb
{
  namespace net
  {
    class MpiGroup
    {
      public:
        /**
         * Default c'tor - initialises equivalent to MPI_GROUP_NULL
         */
        MpiGroup();

        /**
         * Returns the local rank within the group
         * @return
         */
        int Rank() const;

        /**
         * Returns the size of the group
         * @return
         */
        int Size() const;

        /**
         * Exclude the provided ranks
         * @param ranksToExclude
         * @return
         */
        MpiGroup Exclude(const std::vector<proc_t>& ranksToExclude);
        /**
         * Include the provided ranks
         * @param ranksToExclude
         * @return
         */
        MpiGroup Include(const std::vector<proc_t>& ranksToInclude);

        /**
         * Implicit cast to the underlying MPI_group
         * @return
         */
        operator MPI_Group() const
        {
          return *groupPtr;
        }

      private:
        // Allow Communicators access to the c'tor.
        friend class MpiCommunicator;

        // Direct construction.
        /**
         * Construct from an MPI_Group
         * @param grp
         * @param own - Whether this instance is responsible for deleting the
         * group when all copies are destroyed.
         */
        MpiGroup(MPI_Group grp, bool own);

        boost::shared_ptr<MPI_Group> groupPtr;
    };
  }
}

#endif /* HEMELB_NET_MPIGROUP_H */
