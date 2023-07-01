const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const session = require('express-session');
const passport = require('passport');
const LocalStrategy = require('passport-local').Strategy;
const bcrypt = require('bcryptjs');
const blogRoutes = require('./routes/blog.server.routes')
const { User } = require('./models')

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

app.use(bodyParser.urlencoded({ extended: false }));
app.use(session({
  secret: 'your-session-secret',
  resave: false,
  saveUninitialized: false
}));
app.use(passport.initialize());
app.use(passport.session());

// Passport configuration
passport.use(new LocalStrategy(
    async function(username, password, done) {
        const users = await User.findAll()
        const user = users.find(user => user.username === username);

        if (!user) {
        return done(null, false, { message: 'Incorrect username.' });
        }

        bcrypt.compare(password, user.password, (err, res) => {
        if (res) {
            // Passwords match
            return done(null, user);
        } else {
            // Passwords don't match
            return done(null, false, { message: 'Incorrect password.' });
        }
        });
    }
));

passport.serializeUser((user, done) => {
    done(null, user.id);
});

passport.deserializeUser( async (id, done) => {
    const users = await User.findAll()
    const user = users.find(user => user.id === id);
    done(null, user);
});


// Routes
blogRoutes(app)

app.get('/', (req, res) => {
    res.send('Hello from the backend!');
});

app.post('/api/v1/login/', (req, res) => {
    passport.authenticate('local', (err, user, info) => {
      if (err) {
        return res.status(500).json({ error: err });
      }
      if (!user) {
        return res.status(401).json({ authenticated: false, message: info.message });
      }
      req.logIn(user, (err) => {
        if (err) {
          return res.status(500).json({ error: err });
        }
        return res.status(200).json({ authenticated: true, username: user.username });
      });
    })(req, res);
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
