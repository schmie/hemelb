// 
// Copyright (C) University College London, 2007-2012, all rights reserved.
// 
// This file is part of HemeLB and is CONFIDENTIAL. You may not work 
// with, install, use, duplicate, modify, redistribute or share this
// file, or any part thereof, other than as allowed by any agreement
// specifically made by you with University College London.
// 

/*
 * Matrix3D.cc
 *
 *  Created on: May 21, 2012
 *      Author: mobernabeu
 */

#include "util/Matrix3D.h"

namespace hemelb
{
  namespace util
  {

    distribn_t* Matrix3D::operator [](const unsigned int row)
    {
      return matrix[row];
    }

    void Matrix3D::operator*=(distribn_t value)
    {
      for (unsigned row = 0; row < 3; row++)
      {
        for (unsigned column = 0; column < 3; column++)
        {
          matrix[row][column] *= value;
        }
      }
    }

    void Matrix3D::addDiagonal(distribn_t value)
    {
      for (unsigned row = 0; row < 3; row++)
      {
        matrix[row][row] += value;
      }
    }

    void Matrix3D::timesVector(const util::Vector3D<double>& multiplier, util::Vector3D<double>& result) const
    {
      for (unsigned row = 0; row < 3; row++)
      {
        result[row] = 0.0;
        for (unsigned column = 0; column < 3; column++)
        {
          result[row] += matrix[row][column] * multiplier[column];
        }
      }
    }

    Matrix3D Matrix3D::operator*(distribn_t scalarValue) const
    {
      Matrix3D returnMatrix;
      for (unsigned rowIndex = 0; rowIndex < 3; ++rowIndex)
      {
        for (unsigned columnIndex = 0; columnIndex < 3; ++columnIndex)
        {
          returnMatrix[rowIndex][columnIndex] = scalarValue * matrix[rowIndex][columnIndex];
        }
      }
      return returnMatrix;
    }


  } /* namespace util */
} /* namespace hemelb */
