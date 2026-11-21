# T-581: Redmine set up to hold the TODO files' tickets (statuses, priorities, trackers, a role, every transition,
# the ticket fields, the projects, claude-sessions' membership). Idempotent. Holds no key or password. Run on roverbyteseer:
#   docker exec -i redmine-app sh -c 'cat > /tmp/s.rb && SECRET_KEY_BASE="$REDMINE_SECRET_KEY_BASE" bundle exec rails runner -e production /tmp/s.rb' < redmine_setup_tickets.rb
# (only the server's own entrypoint sets SECRET_KEY_BASE).
Setting.text_formatting = 'common_mark'
Setting.rest_api_enabled = '1'
Setting.default_projects_public = '0'

STATUSES = [['Ready', false], ['In progress', false], ['Blocked', false], ['Needs decision', false],
            ['Deferred', false], ['Closed', true], ['Superseded', true]]
statuses = STATUSES.each_with_index.map do |(name, closed), i|
  s = IssueStatus.find_by(name: name) || IssueStatus.new(name: name)
  s.is_closed = closed
  s.position = i + 1
  s.save!
  s
end
ready = statuses.first

%w[Low Normal High Urgent].each_with_index do |name, i|
  pr = IssuePriority.find_by(name: name) || IssuePriority.new(name: name)
  pr.position = i + 1
  pr.is_default = (name == 'Normal')
  pr.active = true
  pr.save!
end

trackers = %w[Job Bug].map do |name|
  t = Tracker.find_by(name: name) || Tracker.new(name: name)
  t.default_status = ready
  t.save!
  t
end

role = Role.find_by(name: 'Ticket keeper') || Role.new(name: 'Ticket keeper')
role.permissions = %i[view_issues add_issues edit_issues add_issue_notes copy_issues manage_issue_relations
                      manage_subtasks manage_versions view_issue_watchers]
role.issues_visibility = 'all'
role.assignable = true
role.save!

trackers.each do |t|
  ([nil] + statuses).each do |from|
    statuses.each do |to|
      next if from == to
      WorkflowTransition.find_or_create_by!(role_id: role.id, tracker_id: t.id,
                                            old_status_id: from ? from.id : 0, new_status_id: to.id)
    end
  end
end

# The fields a ticket row is rebuilt from (tools/tickets.py): the id, where it sits, how it was written,
# the commits that closed it, a WIP claim's branch, and each table column beyond "what".
FIELDS = [
  ['Ticket', 'string', true, 'T-580, C-397: permanent, unpadded'],
  ['Run', 'int', false, 'which table in the TODO file'],
  ['Order', 'int', false, 'its place in the file'],
  ['Shown as', 'string', false, 'the id cell as written, when not the plain form'],
  ['Commits', 'text', false, 'repo@sha, one per line'],
  ['Branch', 'string', false, 'a WIP claim'],
  ['Where', 'text', false, 'column'], ['From', 'text', false, 'column'], ['Blocked on', 'text', false, 'column'],
  ['Why not yet', 'text', false, 'column'], ['Closed by', 'text', false, 'column'],
  ['State', 'text', false, 'column'], ['See', 'text', false, 'column'],
  ['Extra cells', 'text', false, 'cells beyond the table, JSON'], ['Row tail', 'string', false, 'a row not ending in " |"'],
]
FIELDS.each_with_index do |(name, fmt, req, desc), i|
  f = IssueCustomField.find_by(name: name) || IssueCustomField.new(name: name, field_format: fmt)
  f.is_required = req
  f.is_for_all = true
  f.is_filter = %w[Ticket Commits Branch].include?(name)
  f.searchable = fmt != 'int'
  f.visible = true
  f.editable = true
  f.description = desc
  f.position = i + 1
  f.text_formatting = 'full' if fmt == 'text'
  f.trackers = trackers
  f.save!
end

def project(ident, name, desc, parent = nil)
  p = Project.find_by(identifier: ident) || Project.new(identifier: ident)
  p.name = name
  p.description = desc
  p.is_public = false
  p.save!
  p.set_parent!(parent) if parent && p.parent != parent
  p.enabled_module_names = %w[issue_tracking]
  p.trackers = Tracker.where(name: %w[Job Bug]).to_a
  p.save!
  p
end

top = project('context-content', 'CONTEXT / CONTENT', 'The DAEMONS projects. Its TODO files are mirrors of these tickets (T-581).')
kids = [project('daemons', 'DAEMONS', 'docs/TODO.md: T- tickets, the game and its docs.', top),
        project('companion', 'daemons-companion', 'TODO.md: C- tickets, the app, server and devices.', top),
        # C-411's point 1 (prefix E: the user, 2026-11-20, by multiple choice): EUDAIMONIA's own tickets, E-1 onward
        project('eudaimonia', 'daemons-eudaimonia', 'TODO.md: E- tickets, EUDAIMONIA (the site) and the game in a browser.', top)]

u = User.find_by_login('claude-sessions')
[top, *kids].each do |p|
  m = Member.find_by(project_id: p.id, user_id: u.id) || Member.new(project: p, principal: u)
  m.role_ids = (m.role_ids | [role.id])
  m.save!
end

puts "SETUP statuses=#{IssueStatus.count} trackers=#{Tracker.pluck(:name).join(',')} fields=#{IssueCustomField.count} " \
     "projects=#{Project.pluck(:identifier).join(',')} transitions=#{WorkflowTransition.count} members=#{Member.count} " \
     "format=#{Setting.text_formatting}"
