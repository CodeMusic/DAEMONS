# Run on roverbyteseer like tools/redmine_setup_tickets.rb (after it). It prints each lane's key as 'KEY <LANE> <key>':
# capture that into ~/.redmine.env as REDMINE_KEY_<LANE>=<key> (mode 600) without showing it. Holds no key itself.
# T-581: one Redmine user per session lane (the user, 2026-11-17, by multiple choice; devices split by type).
# Not admin, no mail; a random password never kept -- each signs in with its own key. Idempotent.
LANES = {
  'game' => 'engine, maps, mechanics', 'story' => 'writing, books, narrative', 'audio' => 'music and sounds',
  'art' => 'sprites, buildings, covers', 'app' => 'the companion app and site', 'hub' => 'the server, the Tiiny, the mind',
  'esp32' => 'ESP32 boards: T-Watch Ultra, the handhelds', 'pi-zero' => 'Pi Zero devices: the Cardputer Zero',
  'playground' => 'daemons-eudaimonia: EUDAIMONIA, and the game in a browser', 'docs' => 'manuals, READMEs, wikis, release docs',
  'ops' => 'roverbyteseer, Redmine, backups, the nightly mirror',
}
role = Role.find_by!(name: 'Ticket keeper')
projects = Project.where(identifier: %w[context-content daemons companion eudaimonia]).to_a
LANES.each do |lane, what|
  login = "lane-#{lane}"
  u = User.find_by_login(login) || User.new
  u.login = login
  u.firstname = 'Lane'
  u.lastname = lane
  u.mail = "#{login}@roverbyteseer.invalid"
  u.admin = false
  u.status = User::STATUS_ACTIVE
  u.mail_notification = 'none'
  if u.new_record?
    pw = SecureRandom.alphanumeric(40)
    u.password = pw
    u.password_confirmation = pw
  end
  u.save!
  projects.each do |p|
    m = Member.find_by(project_id: p.id, user_id: u.id) || Member.new(project: p, principal: u)
    m.role_ids = (m.role_ids | [role.id])
    m.save!
  end
  STDOUT.print "KEY #{lane.upcase.tr('-', '_')} #{u.api_key}\n"
end
STDOUT.print "LANES #{User.where('login LIKE ?', 'lane-%').count} members=#{Member.count}\n"
