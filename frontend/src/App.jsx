
import { useState } from 'react'
import './App.css'

function App() {
  const [selectedCareer, setSelectedCareer] = useState('')
  const [java, setJava] = useState(50)
  const [dsa, setDsa] = useState(30)
  const [dbms, setDbms] = useState(40)
  const [hours, setHours] = useState(2)
  const [simulationHours, setSimulationHours] = useState(2)
  const [submitted, setSubmitted] = useState(false)

  const skills = [
    { name: 'Java', score: java },
    { name: 'Data Structures & Algorithms', score: dsa },
    { name: 'DBMS', score: dbms }
  ]

  const weakSkills = skills.filter(skill => skill.score < 40)
  const overallScore = Math.round(
    skills.reduce((total, skill) => total + skill.score, 0) / skills.length
  )

  const learningTopics = {
    Java: ['Java Basics and Syntax', 'OOP Concepts', 'Collections Framework', 'Exception Handling'],
    'Data Structures & Algorithms': ['Arrays and Strings', 'Searching and Sorting', 'Linked Lists and Stacks', 'Trees and Graphs', 'Dynamic Programming'],
    DBMS: ['Database Fundamentals', 'SQL Queries', 'Normalization', 'Transactions and Joins']
  }

  const roadmap = [
    ...weakSkills.map(skill => skill.name),
    ...skills.filter(skill => skill.score >= 40 && skill.score < 70).map(skill => skill.name),
    'Build Practical Projects'
  ]

  const learningWork = weakSkills.length * 20 + 30
  const estimatedDays = Math.max(1, Math.ceil(learningWork / Math.max(1, hours)))
  const simulatedDays = Math.max(1, Math.ceil(learningWork / Math.max(1, simulationHours)))

  function handleSubmit() {
    if (!selectedCareer) {
      alert('Please select a career first!')
      return
    }
    setSubmitted(true)
    setSimulationHours(hours)
  }

  return (
    <div>
      <nav className="navbar">
        <div className="brand">
          <h2>DSSAM</h2>
          <span>Distributed Skill Simulation Analysis Model</span>
        </div>
        <div>
          <a href="#home">Home</a>
          <a href="#careers">Careers</a>
          <a href="#dashboard">Dashboard</a>
          <a href="#features">Features</a>
        </div>
      </nav>

      <section className="hero" id="home">
        <div className="hero-content">
          <p className="tag">INTELLIGENT CAREER PLANNING SYSTEM</p>
          <h1>Analyze Your Skills. Simulate Your Growth.</h1>
          <p>
            DSSAM helps learners understand their skill gaps,
            explore personalized learning paths and plan their
            journey towards their desired career.
          </p>
          <a href="#careers" className="main-btn">Get Started</a>
        </div>

        <div className="hero-card">
          <h3>Your Career Progress</h3>
          <p>Java <span>75%</span></p>
          <div className="progress"><div style={{ width: '75%' }} /></div>
          <p>DSA <span>45%</span></p>
          <div className="progress"><div style={{ width: '45%' }} /></div>
          <p>DBMS <span>60%</span></p>
          <div className="progress"><div style={{ width: '60%' }} /></div>
        </div>
      </section>

      <section className="career-section" id="careers">
        <p className="tag">START YOUR JOURNEY</p>
        <h2>Choose Your Career Goal</h2>
        <p>Select the career you want to prepare for.</p>

        <div className="career-grid">
          {['Software Developer', 'Frontend Developer', 'Data Analyst'].map(career => (
            <div
              key={career}
              className={`career-card ${selectedCareer === career ? 'selected' : ''}`}
              onClick={() => {
                setSelectedCareer(career)
                setSubmitted(false)
              }}
            >
              <h3>{career}</h3>
              <p>Explore skills required for this career.</p>
              <span>{selectedCareer === career ? 'Selected ✓' : 'Select Career →'}</span>
            </div>
          ))}
        </div>
      </section>

      {selectedCareer && (
        <section className="assessment-section">
          <p className="tag">STEP 2</p>
          <h2>Assess Your Skills</h2>
          <p>Rate your current knowledge from 0 to 100.</p>

          <div className="assessment-card">
            <label>Java: {java}%</label>
            <input type="range" min="0" max="100" value={java}
              onChange={e => setJava(Number(e.target.value))} />

            <label>DSA: {dsa}%</label>
            <input type="range" min="0" max="100" value={dsa}
              onChange={e => setDsa(Number(e.target.value))} />

            <label>DBMS: {dbms}%</label>
            <input type="range" min="0" max="100" value={dbms}
              onChange={e => setDbms(Number(e.target.value))} />

            <label>Daily study hours</label>
            <input type="number" min="1" max="12" value={hours}
              onChange={e => setHours(Math.max(1, Number(e.target.value)))} />

            <button className="main-btn" onClick={handleSubmit}>
              Generate My Dashboard
            </button>
          </div>
        </section>
      )}

      {submitted && (
        <>
          <section className="dashboard-section" id="dashboard">
            <p className="tag">YOUR PERSONAL DASHBOARD</p>
            <h2>Learning Performance Overview</h2>
            <p>Career Goal: <strong>{selectedCareer}</strong></p>

            <div className="dashboard-grid">
              <div className="dashboard-card">
                <p>Overall Skill Score</p>
                <h2>{overallScore}%</h2>
              </div>
              <div className="dashboard-card">
                <p>Weak Skills</p>
                <h2>{weakSkills.length}</h2>
              </div>
              <div className="dashboard-card">
                <p>Daily Study Hours</p>
                <h2>{hours} hrs</h2>
              </div>
              <div className="dashboard-card">
                <p>Estimated Learning Time</p>
                <h2>{estimatedDays} days</h2>
              </div>
            </div>

            <h3 className="skill-heading">Your Skill Performance</h3>
            <div className="skill-performance">
              {skills.map(skill => (
                <div className="skill-row" key={skill.name}>
                  <div>
                    <strong>{skill.name}</strong>
                    <span>{skill.score}%</span>
                  </div>
                  <div className="progress">
                    <div style={{ width: `${skill.score}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className="simulation-section">
            <p className="tag">WHAT-IF SIMULATION</p>
            <h2>Simulate Your Learning Progress</h2>
            <p>What if you change your daily study hours?</p>

            <div className="simulation-card">
              <h3>Daily Study Hours: {simulationHours}</h3>
              <input
                type="range"
                min="1"
                max="8"
                value={simulationHours}
                onChange={e => setSimulationHours(Number(e.target.value))}
              />

              <div className="simulation-result">
                <p>Estimated learning time</p>
                <h1>{simulatedDays} Days</h1>
                <p>
                  At {simulationHours} hours of study per day.
                </p>
              </div>

              <div className="comparison">
                <div>
                  <p>Current plan</p>
                  <h3>{estimatedDays} days</h3>
                  <span>{hours} hours/day</span>
                </div>
                <div>
                  <p>Simulated plan</p>
                  <h3>{simulatedDays} days</h3>
                  <span>{simulationHours} hours/day</span>
                </div>
              </div>

              <p className="small-note">
                Estimates are illustrative and based on a simple study-time
                formula. They are not guaranteed completion dates.
              </p>
            </div>
          </section>

          <section className="roadmap-section">
            <p className="tag">YOUR PERSONALIZED PLAN</p>
            <h2>Learning Roadmap</h2>
            <p>Follow these steps to move towards your career goal.</p>

            <div className="roadmap-container">
              {roadmap.map((item, index) => (
                <div className="roadmap-item" key={item}>
                  <div className="roadmap-number">{index + 1}</div>
                  <div className="roadmap-content">
                    <h3>{item}</h3>
                    <p>
                      {item === 'Build Practical Projects'
                        ? 'Apply your knowledge by building real-world projects.'
                        : 'Focus on the following learning topics:'}
                    </p>

                    {learningTopics[item] && (
                      <ul>
                        {learningTopics[item].map(topic => (
                          <li key={topic}>{topic}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </section>
        </>
      )}

      <section className="features-section" id="features">
        <h2>Why Choose DSSAM?</h2>
        <div className="features-grid">
          <div className="feature-card">
            <h3>Skill Analysis</h3>
            <p>Understand your current skill level.</p>
          </div>
          <div className="feature-card">
            <h3>Learning Simulation</h3>
            <p>Explore different learning scenarios.</p>
          </div>
          <div className="feature-card">
            <h3>Career Planning</h3>
            <p>Prepare step by step for your target career.</p>
          </div>
        </div>
      </section>

      <footer>
        <h2>DSSAM</h2>
        <p>Distributed Skill Simulation Analysis Model</p>
        <p>Your skills. Your growth. Your career.</p>
      </footer>
    </div>
  )
}

export default App
