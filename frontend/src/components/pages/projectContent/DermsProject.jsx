import Badge from '../../reusable/Badge.js'

export default (
    <div className='max-w-4xl mx-auto p-4'>
        <h1 className="text-2xl md:text-4xl font-bold">Resource Data Management System</h1>
        <h2 className="text-l md:text-xl mb-2"><span className="font-bold">Role: </span>Software Engineer</h2>

        <div className="mb-6">
            <Badge color="purple">AWS Integrations</Badge>
            <Badge color="purple">Software Archirecture</Badge>
            <Badge color="purple">Client Management</Badge>
            <Badge color="purple">Mentoring</Badge>
        </div>

        <h2 className="text-2xl font-bold mb-4">Project Overview</h2>
        <p className="mb-4">
        Worked as a software engineer on the RDMS (Resource Data Management System), a web application designed for the Australian Defence. The application effectively managed and monitored various resource metering devices, including electricity, water, gas, and LPG, drawing valuable insights from the ingested metering data. Implemented functionalities for adding, swapping, and removing meters, streamlining resource management processes. Developed the RDMS Accounts section, which handled payment and invoicing, automating the workflow and enhancing efficiency by integrating scanned invoice PDFs.
        </p>

        <h2 className="text-2xl font-bold mb-4">Key Responsibilities</h2>
        <ul className="list-disc pl-6 mb-4">
            <li>
          Architected the project structure and made crucial design decisions, including database structure, backend, and frontend design.
            </li>
            <li>
          Mentored an intern, <span className="text-highlight">facilitating their growth from intern to junior developer.</span>
            </li>
            <li>
          Set up AWS infrastructure for email ingestion, PDF extraction, and third-party scanning, leveraging AWS SES, S3, and Lambda.
            </li>
            <li>
          Actively engaged in client communication, <span className="text-highlight">gathering requirements, setting expectations, and managing delivery deadlines.</span>
            </li>
            <li>
          Presented development progress to clients <span className="text-highlight">for feedback and validation.</span>
            </li>
            <li>
          Undertook typical software engineer responsibilities, such as feature development and bug fixing.
            </li>
        </ul>

        <h2 className="text-2xl font-bold mb-4">Skills Acquired</h2>
        <ul className="list-disc pl-6 mb-4">
            <li>
          Proficiency in architectural design, encompassing database structure, backend, and frontend components.
            </li>
            <li>
          Mentorship and leadership skills, <span className="text-highlight">fostering the growth of an intern into a junior developer.</span>
            </li>
            <li>
          AWS infrastructure setup and management, involving email ingestion, PDF processing, and third-party integration.
            </li>
            <li>
          Effective client communication <span className="text-highlight">and requirement gathering.</span>
            </li>
            <li>
          Presentation and client feedback incorporation into the development process.
            </li>
        </ul>

        <h2 className="text-2xl font-bold mb-4">Result</h2>
        <p className="mb-4">
        RDMS successfully streamlined resource monitoring, payment, and invoicing processes for the Australian Defence, significantly improving workflow efficiency. Integration of data visualization techniques provided valuable insights into resource data, aiding in better resource management.
        </p>

        <h2 className="text-2xl font-bold mb-4">Professional Growth</h2>
        <p className="mb-4">
        Played a pivotal role in architectural decision-making, project leadership, and client interaction, contributing significantly to professional growth. The experience gained in AWS infrastructure setup and management further enhanced skills in cloud technology. Mentoring the intern to become a qualified junior developer was a rewarding professional accomplishment.
        </p>

    </div>
)
