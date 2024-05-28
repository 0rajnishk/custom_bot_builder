import React from 'react'
import ListItem from '@mui/material/ListItem'
import ListItemIcon from '@mui/material/ListItemIcon'
import ListItemText from '@mui/material/ListItemText'
import DashboardIcon from '@mui/icons-material/Dashboard'
import ChatIcon from '@mui/icons-material/ChatSharp'
import PeopleIcon from '@mui/icons-material/People'
import BarChartIcon from '@mui/icons-material/BarChart'
// import LayersIcon from '@mui/icons-material/Layers'
import { Link } from 'react-router-dom'

export const mainListItems = (
  <div>
    <ListItem button component={Link} to='/dashboard'>
      <ListItemIcon>
        <DashboardIcon />
      </ListItemIcon>
      <ListItemText primary='Dashboard' />
    </ListItem>

    <ListItem button component={Link} to='/bot'>
      <ListItemIcon>
        <ChatIcon />
      </ListItemIcon>
      <ListItemText primary='bot' />
    </ListItem>

    <ListItem button component={Link} to='/integrations'>
      <ListItemIcon>
        <PeopleIcon />
      </ListItemIcon>
      <ListItemText primary='integrations' />
    </ListItem>

    <ListItem button component={Link} to='/integrations'>
      <ListItemIcon>
        <BarChartIcon />
      </ListItemIcon>
      <ListItemText primary='Reports' />
    </ListItem>
  </div>
)

// export const secondaryListItems = (
//   <div>
//     <ListSubheader inset>Sub List</ListSubheader>
//     <ListItem button>
//       <ListItemIcon>
//         <AssignmentIcon />
//       </ListItemIcon>
//       <ListItemText primary='More List' />
//     </ListItem>
//   </div>
// )
