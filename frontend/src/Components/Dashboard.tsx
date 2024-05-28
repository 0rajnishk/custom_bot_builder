import React, { useState } from 'react'
import { BrowserRouter as Router, Switch, Route, Redirect } from 'react-router-dom'
import { useAuthState } from 'react-firebase-hooks/auth'
import { styled, createTheme, ThemeProvider } from '@mui/material/styles'
import MuiDrawer from '@mui/material/Drawer'
import Box from '@mui/material/Box'
import MuiAppBar, { AppBarProps as MuiAppBarProps } from '@mui/material/AppBar'
import Toolbar from '@mui/material/Toolbar'
import List from '@mui/material/List'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'
import IconButton from '@mui/material/IconButton'
import Badge from '@mui/material/Badge'
import Container from '@mui/material/Container'
import Grid from '@mui/material/Grid'
import Paper from '@mui/material/Paper'
import Avatar from '@mui/material/Avatar'
import MenuIcon from '@mui/icons-material/Menu'
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft'
import NotificationsIcon from '@mui/icons-material/Notifications'

import { mainListItems } from './listItems'
import SignOut from './SignOut'
import Footer from './Footer'
import Title from './Title'
import NewBotForm from './NewBotForm'
import ChatBot from './ChatBot'

import { auth } from '../Firebase'

const drawerWidth = 240

interface AppBarProps extends MuiAppBarProps {
  open?: boolean
}

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open'
})<AppBarProps>(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(['width', 'margin'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen
    })
  })
}))

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(({ theme, open }) => ({
  '& .MuiDrawer-paper': {
    position: 'relative',
    whiteSpace: 'nowrap',
    width: drawerWidth,
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen
    }),
    boxSizing: 'border-box',
    ...(!open && {
      overflowX: 'hidden',
      transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen
      }),
      width: theme.spacing(7),
      [theme.breakpoints.up('sm')]: {
        width: theme.spacing(9)
      }
    })
  }
}))

const mdTheme = createTheme()

export default function Dashboard() {
  const [currentUser] = useAuthState(auth)
  const [open, setOpen] = useState(true)
  const toggleDrawer = () => setOpen((prev) => !prev)

  return (
    <Router>
      <ThemeProvider theme={mdTheme}>
        <Box sx={{ display: 'flex' }}>
          <AppBar position='absolute' open={open}>
            <Toolbar
              sx={{
                pr: '24px'
              }}
            >
              <IconButton
                edge='start'
                color='inherit'
                aria-label='open drawer'
                onClick={toggleDrawer}
                sx={{
                  marginRight: '36px',
                  ...(open && { display: 'none' })
                }}
              >
                <MenuIcon />
              </IconButton>
              <Typography component='h1' variant='h6' color='inherit' noWrap sx={{ flexGrow: 1 }}>
                Welcome {currentUser.displayName}!
              </Typography>
              <IconButton color='inherit' sx={{ mr: 2 }}>
                <Badge badgeContent={4} color='secondary'>
                  <NotificationsIcon />
                </Badge>
              </IconButton>
              <Avatar alt={currentUser.displayName} src={currentUser.photoURL} sx={{ mr: 2 }} />
              <SignOut />
            </Toolbar>
          </AppBar>
          <Drawer variant='permanent' open={open}>
            <Toolbar
              sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'flex-end',
                px: [1]
              }}
            >
              <IconButton onClick={toggleDrawer}>
                <ChevronLeftIcon />
              </IconButton>
            </Toolbar>
            <Divider />
            <List>{mainListItems}</List>
            <Divider />
          </Drawer>
          <Box
            component='main'
            sx={{
              backgroundColor: (theme) =>
                theme.palette.mode === 'light' ? theme.palette.grey[100] : theme.palette.grey[900],
              flexGrow: 1,
              height: '100vh',
              overflow: 'auto'
            }}
          >
            <Toolbar />
            <Container maxWidth='lg' sx={{ mt: 4, mb: 4 }}>
              <Grid container spacing={3}>
                <Switch>
                  {/* Dashboard */}
                  <Route path='/dashboard'>
                    <Grid item xs={12} md={8} lg={9}>
                      <Paper
                        sx={{
                          p: 2,
                          display: 'flex',
                          flexDirection: 'column',
                          height: 550
                        }}
                      >
                        <Title>Bot Builder</Title>
                        <div>
                          <p>
                            Welcome to the Bot Builder! Here you can create your own chatbot and try them.
                          </p>
                          <NewBotForm />
                        </div>
                      </Paper>
                    </Grid>
                  </Route>
                  {/* bot */}
                  <Route path='/bot'>
                    <Grid item xs={12} md={8} lg={9}>
                      <Paper
                        sx={{
                          p: 2,
                          display: 'flex',
                          flexDirection: 'column',
                          height: 820
                        }}
                      >
                        <Title>bot</Title>
                          <p>
                            You don&apos;t have any bot yet. Create one from the dashboard.
                          </p>
                          <ChatBot />
                      </Paper>
                    </Grid>
                  </Route>
                  {/* Integrations */}
                  <Route path='/integrations'>
                    <Grid item xs={12} md={8} lg={9}>
                      <Paper
                        sx={{
                          p: 2,
                          display: 'flex',
                          flexDirection: 'column',
                          height: 940,
                        }}
                      >
                        <Title>How to integrate the bot</Title>
                        <div>
                          <h1>Upload PDF and Create Chatbot</h1>
                          <p>
                            To upload a PDF and create a chatbot, follow these steps:
                            <ol>
                              <li>Create a form with a file input for the PDF and a text input for the chatbot name.</li>
                              <li>Use the following endpoint to upload the PDF and create the chatbot:
                                <pre>
                                  POST /upload
                                  <br />
                                  Form Data:
                                  <br />
                                  - file: (PDF File)
                                  <br />
                                  - chatbot_name: (Chatbot Name)
                                </pre>
                              </li>
                            </ol>
                          </p>

                          <h2>Query Chatbot</h2>
                          <p>
                            To query the chatbot, follow these steps:
                            <ol>
                              <li>Create a form with a text input for the chatbot name and another text input for your query.</li>
                              <li>Use the following endpoint to query the chatbot:
                                <pre>
                                  POST /query_chatbot/&#123;chatbot_name&#125;
                                  <br />
                                  JSON Body:
                                  <br />
                                  - query: (Your Query)
                                </pre>
                              </li>
                            </ol>
                          </p>

                          <h2>Get Chatbot Details</h2>
                          <p>
                            To get the details of the chatbot, follow these steps:
                            <ol>
                              <li>Create a form with a text input for the chatbot name.</li>
                              <li>Use the following endpoint to get the chatbot details:
                                <pre>
                                  GET /get_chatbot/&#123;chatbot_name&#125;
                                </pre>
                              </li>
                            </ol>
                          </p>
                        </div>
                      </Paper>
                    </Grid>
                  </Route>
                  {/* Redirect none matches routes */}
                  <Route render={() => <Redirect to='/dashboard' />} />
                </Switch>
              </Grid>
              <Footer />
            </Container>
          </Box>
        </Box>
      </ThemeProvider>
    </Router>
  )
}
